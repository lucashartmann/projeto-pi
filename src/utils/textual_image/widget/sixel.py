"""Provides a Textual `Widget` to render images as Sixels (<https://en.wikipedia.org/wiki/Sixel>) in the terminal.

Note on Performance and Limitations:
    Sixel support in Textual requires using `render_lines()` directly to inject terminal control
    sequences, which bypasses the normal rendering pipeline. This is necessary because:
    1. Sixel data must be positioned based on the visible crop region (only available in render_lines)
    2. Terminal control sequences must be injected directly into the rendering stream
    
    This approach can cause some flickering during scrolling and style changes, especially with
    large images. The implementation includes several optimizations to mitigate this:
    - Multi-level caching (direct cache + LRU caches for scaled images and sixel data)
    - Background generation with debouncing for large images
    - Intelligent fallback to nearby cached regions during scrolling
    - Pre-generation of full images for large static content
    
    For mostly static images, performance should be acceptable. For dynamic content with frequent
    scrolling, consider using TGP (Terminal Graphics Protocol) if available, which performs better.
"""

import logging
from collections import OrderedDict
from typing import IO, Iterable, NamedTuple, Optional, Tuple

from PIL import Image as PILImage
from rich.console import Console, ConsoleOptions, RenderResult
from rich.control import Control
from rich.measure import Measurement
from rich.segment import ControlType, Segment
from rich.style import Style
from textual.app import ComposeResult
from textual.dom import NoScreen
from textual.geometry import Region, Size
from textual.strip import Strip
from textual.widget import Widget
from typing_extensions import override

from textual_image._geometry import ImageSize
from textual_image._pixeldata import PixelData
from textual_image._sixel import image_to_sixels
from textual_image._terminal import CellSize, get_cell_size
from textual_image._utils import StrOrBytesPath
from textual_image.widget._base import Image as BaseImage

logger = logging.getLogger(__name__)


_NULL_STYLE = Style()


class _CachedSixels(NamedTuple):
    image: StrOrBytesPath | IO[bytes] | PILImage.Image
    content_crop: Region
    content_size: Size
    terminal_sizes: CellSize
    sixel_data: str

    def is_hit(
        self,
        image: StrOrBytesPath | IO[bytes] | PILImage.Image,
        content_crop: Region,
        content_size: Size,
        terminal_sizes: CellSize,
    ) -> bool:
        return (
            image == self.image
            and content_crop == self.content_crop
            and content_size == self.content_size
            and terminal_sizes == self.terminal_sizes
        )


class _NoopRenderable:
    """Image renderable rendering nothing.

    Used by the Sixel image as placeholder.
    Rendering the Sixel renderable doesn't work with Textual as it relies on printable segments.
    Instead, Sixel data is injected into the rendering process. To keep our base class happy, we use this class
    as renderable passed to it.
    """

    def __init__(
        self,
        image: StrOrBytesPath | IO[bytes] | PILImage.Image,
        width: int | str | None = None,
        height: int | str | None = None,
    ) -> None:
        pass

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        yield Segment("")

    def __rich_measure__(self, console: Console, options: ConsoleOptions) -> Measurement:
        return Measurement(0, 0)

    def cleanup(self) -> None:
        pass


class Image(BaseImage, Renderable=_NoopRenderable):
    """Textual `Widget` to render images as Sixels (<https://en.wikipedia.org/wiki/Sixel>) in the terminal."""

    @override
    @BaseImage.image.setter  # type: ignore
    def image(self, value: StrOrBytesPath | IO[bytes] | PILImage.Image | None) -> None:
        super(__class__, type(self)).image.fset(self, value)  # type: ignore
        # If image is being removed, mark child widget for clearing
        if value is None:
            try:
                child = self.query_one(_ImageSixelImpl)
                child._needs_clear = True
            except Exception:
                pass
        self.refresh(recompose=True)

    def compose(self) -> ComposeResult:
        """Called by Textual to create child widgets."""
        yield _ImageSixelImpl(self.image)


class _ImageSixelImpl(Widget, can_focus=False, inherit_css=False):
    """Widget implementation injecting Sixel data into the rendering process.

    This class is meant to be used only by `textual_image.widgets.sixel.Image`.
    It creates and renders Sixel data.

    It is done in this child widget to simplify the process -- this class assumes it never has to render any borders or spacings,
    but only the parent will if required by the user.
    We assume `self.region == self.content_region` in this class, which allows to the `crop` parameter in `render_lines()` directly
    on our image data without having to deal with gutters, as well as moving the cursor after rendering the sixel data to an easily
    determinable position.
    """

    DEFAULT_CSS = """
    _ImageData {
        width: 100%;
        height: 100%;
    }
    """

    @override
    def __init__(
        self,
        image: StrOrBytesPath | IO[bytes] | PILImage.Image | None = None,
    ) -> None:
        super().__init__()
        self.image = image
        self._cached_sixels: _CachedSixels | None = None

        # LRU caches
        self._scaled_lru: "OrderedDict[Tuple, PixelData]" = OrderedDict()
        self._sixel_lru: "OrderedDict[Tuple, str]" = OrderedDict()
        self._scaled_cache_size: int = 3
        self._sixel_cache_size: int = 8

        # Debounce / background generation
        self._debounce_delay: float = 0.08  # seconds
        self._pending_generation: Optional[Tuple[Region, Size, CellSize]] = None

        # Optional pre-generation behavior (only the full scaled image)
        self._pregen_full_scaled: bool = True
        self._pregen_min_pixels: int = 200000  # pregen if scaled image > 200k pixels
        # Track if we need to clear the area on next render
        self._needs_clear: bool = False

    @override
    def on_unmount(self) -> None:
        """Called when the widget is removed from the DOM.
        
        This ensures the area is cleared when the widget is removed (e.g., when closing a modal).
        """
        self._needs_clear = True
        # Force a refresh to clear the area before unmounting
        try:
            if self.screen and self.screen.is_active:
                self.refresh()
        except (NoScreen, AttributeError):
            pass

    @override
    def render_lines(self, crop: Region) -> list[Strip]:
        # If we need to clear (widget being unmounted) or there's no image, clear the area
        # This removes any leftover Sixel graphics that might remain visible
        try:
            needs_clear = self._needs_clear
            has_image = bool(self.image)
            is_active = self.screen.is_active if hasattr(self, 'screen') else False
            
            if needs_clear or not has_image or not is_active:
                # Reset clear flag before returning
                self._needs_clear = False
                # Clear the area by rendering blank spaces - this removes leftover Sixel graphics
                blank_segment = Segment(" " * crop.width, style=_NULL_STYLE)
                return [Strip([blank_segment], cell_length=crop.width)] * crop.height
        except NoScreen:  # if no screen, return empty list
            return []
        
        # Reset clear flag after checking (in case it was set)
        self._needs_clear = False

        # Inject the sixel data. We can only do it here because we don't know the crop region before.
        terminal_sizes = get_cell_size()

        # First check the small direct cache hit
        if self._cached_sixels and self._cached_sixels.is_hit(self.image, crop, self.content_size, terminal_sizes):
            logger.debug(f"using Sixel data from cache for crop region {crop}")
            sixel_data = self._cached_sixels.sixel_data
        else:
            # Check LRU sixel cache (keyed by crop + sizes)
            sixel_key = (
                id(self.image),
                crop.x,
                crop.y,
                crop.width,
                crop.height,
                self.content_size.width,
                self.content_size.height,
                terminal_sizes.width,
                terminal_sizes.height,
            )

            if sixel_key in self._sixel_lru:
                logger.debug("using sixel from LRU cache")
                sixel_data = self._sixel_lru.pop(sixel_key)
                # move to most recent
                self._sixel_lru[sixel_key] = sixel_data
            else:
                # Attempt to obtain or create a scaled pixeldata from LRU
                scaled_key = (id(self.image), self.content_size.width, self.content_size.height, terminal_sizes.width, terminal_sizes.height)
                if scaled_key in self._scaled_lru:
                    logger.debug("using scaled PixelData from LRU")
                    image_data = self._scaled_lru.pop(scaled_key)
                    self._scaled_lru[scaled_key] = image_data
                else:
                    logger.debug("scaling image for content_size and terminal_sizes")
                    image_data = PixelData(self.image)
                    image_data = self._scale_image(image_data, terminal_sizes)
                    # store in scaled LRU
                    self._scaled_lru[scaled_key] = image_data
                    # trim
                    while len(self._scaled_lru) > self._scaled_cache_size:
                        self._scaled_lru.popitem(last=False)

                    # Optionally pre-generate full scaled sixel in background for large images
                    try:
                        scaled_pixels = image_data.width * image_data.height
                        if self._pregen_full_scaled and scaled_pixels >= self._pregen_min_pixels:
                            full_crop = Region(0, 0, self.content_size.width, self.content_size.height)
                            full_key = (
                                id(self.image),
                                full_crop.x,
                                full_crop.y,
                                full_crop.width,
                                full_crop.height,
                                self.content_size.width,
                                self.content_size.height,
                                terminal_sizes.width,
                                terminal_sizes.height,
                            )
                            if full_key not in self._sixel_lru:
                                # schedule immediate background pregeneration
                                self.set_timer(0, lambda sk=scaled_key, fk=full_key, ad=image_data: self._perform_full_pregen(sk, fk, ad))
                    except Exception:
                        pass

                # Crop and check if we should generate now or schedule
                cropped = self._crop_image(image_data, crop, terminal_sizes)

                # If generation is cheap (small image) or no prior sixel exists, generate now
                approx_pixels = cropped.width * cropped.height
                if approx_pixels < 20000 or not self._sixel_lru:
                    logger.debug("synchronously generating sixel")
                    sixel_data = image_to_sixels(cropped.pil_image)
                    # store in sixel LRU
                    self._sixel_lru[sixel_key] = sixel_data
                    while len(self._sixel_lru) > self._sixel_cache_size:
                        self._sixel_lru.popitem(last=False)
                    self._cached_sixels = _CachedSixels(self.image, crop, self.content_size, terminal_sizes, sixel_data)
                else:
                    # Schedule background generation with debounce and return prior cached sixel if available (fallback)
                    logger.debug("scheduling background sixel generation (debounced)")
                    self._pending_generation = (crop, self.content_size, terminal_sizes)
                    # cancel previous timer by letting it expire and ignoring if outdated; we just set a new one
                    self.set_timer(self._debounce_delay, self._perform_generation)
                    # Use best available fallback: try to find a similar crop region from cache
                    # This helps reduce flickering during scrolling by showing a nearby cached region
                    sixel_data = self._find_best_fallback_sixel(crop, sixel_key)

        sixel_segments = self._get_sixel_segments(sixel_data, crop)
        # Render the sixel in the first line of the crop so the image is drawn early and
        # the content area doesn't show as empty before the image is injected. This
        # reduces visible flicker when the widget moves or the terminal resizes.
        # Empty strips for remaining lines ensure proper layout without interfering with Sixel rendering
        lines = [Strip(sixel_segments, cell_length=crop.width)] + [Strip([])] * (crop.height - 1)
        return lines

    def _scale_image(self, image_data: PixelData, terminal_sizes: CellSize) -> PixelData:
        assert isinstance(self.parent, Image)

        styled_width, styled_height = self.parent._get_styled_size()
        image_size = ImageSize(image_data.width, image_data.height, width=styled_width, height=styled_height)
        pixel_width, pixel_height = image_size.get_pixel_size(
            self.content_size.width, self.content_size.height, terminal_sizes
        )

        return image_data.scaled(pixel_width, pixel_height)

    def _crop_image(self, image: PixelData, crop: Region, terminal_sizes: CellSize) -> PixelData:
        """Crop image data to match the visible crop region.
        
        Args:
            image: The scaled image data to crop.
            crop: The crop region in cell coordinates.
            terminal_sizes: Terminal cell size in pixels.
            
        Returns:
            Cropped image data.
        """
        crop_pixels_left = crop.x * terminal_sizes.width
        crop_pixels_top = crop.y * terminal_sizes.height
        crop_pixels_right = crop.right * terminal_sizes.width
        crop_pixels_bottom = crop.bottom * terminal_sizes.height

        return image.cropped(crop_pixels_left, crop_pixels_top, crop_pixels_right, crop_pixels_bottom)

    def _find_best_fallback_sixel(self, crop: Region, current_key: Tuple) -> str:
        """Find the best fallback Sixel data from cache when exact match isn't available.
        
        This helps reduce flickering during scrolling by showing a nearby cached region
        instead of an empty image while the correct one is being generated.
        
        Args:
            crop: The current crop region.
            current_key: The cache key for the current crop.
            
        Returns:
            Sixel data string, or empty string if no suitable fallback found.
        """
        if not self._sixel_lru:
            return ""
        
        # Try to find a cached region that overlaps with current crop
        # This is better than just using the most recent, as it reduces visual jumps
        best_match = None
        best_overlap = 0
        
        for cached_key, cached_data in self._sixel_lru.items():
            # Check if it's for the same image and size
            if (cached_key[0] == current_key[0] and  # same image
                cached_key[5] == current_key[5] and  # same content_size.width
                cached_key[6] == current_key[6] and  # same content_size.height
                cached_key[7] == current_key[7] and  # same terminal_sizes.width
                cached_key[8] == current_key[8]):   # same terminal_sizes.height
                
                # Calculate overlap between cached region and current crop
                cached_crop = Region(cached_key[1], cached_key[2], cached_key[3], cached_key[4])
                overlap = self._calculate_overlap(crop, cached_crop)
                
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_match = cached_data
        
        # If we found a reasonable overlap (>50%), use it; otherwise use most recent
        if best_match and best_overlap > 0.5:
            logger.debug(f"using fallback sixel with {best_overlap:.0%} overlap")
            return best_match
        elif self._sixel_lru:
            # Fallback to most recent as last resort
            _, sixel_data = next(reversed(self._sixel_lru.items()))
            logger.debug("using most recent sixel as fallback")
            return sixel_data
        
        return ""

    def _calculate_overlap(self, region1: Region, region2: Region) -> float:
        """Calculate overlap ratio between two regions.
        
        Args:
            region1: First region.
            region2: Second region.
            
        Returns:
            Overlap ratio between 0.0 and 1.0.
        """
        # Calculate intersection
        left = max(region1.x, region2.x)
        top = max(region1.y, region2.y)
        right = min(region1.right, region2.right)
        bottom = min(region1.bottom, region2.bottom)
        
        if right <= left or bottom <= top:
            return 0.0
        
        intersection_area = (right - left) * (bottom - top)
        region1_area = region1.width * region1.height
        
        if region1_area == 0:
            return 0.0
        
        return intersection_area / region1_area

    def _get_sixel_segments(self, sixel_data: str, crop: Region) -> Iterable[Segment]:
        """Generate segments with Sixel data and cursor positioning.
        
        Args:
            sixel_data: The Sixel-encoded image data.
            crop: The crop region being rendered (relative to widget content).
            
        Returns:
            Segments containing cursor positioning and Sixel data.
        """
        # According to the class docstring, self.region == self.content_region for this widget.
        # Both are in absolute screen coordinates. The crop is relative to the widget's content,
        # so we add it to get the absolute position on screen.
        try:
            # Use content_region explicitly to ensure we're using the content area (without borders/padding)
            content_region = self.content_region
            abs_x = content_region.x + crop.x
            abs_y = content_region.y + crop.y
        except AttributeError:
            # Fallback to region if content_region is not available
            try:
                abs_x = self.region.x + crop.x
                abs_y = self.region.y + crop.y
            except AttributeError:
                # Last resort: use crop as-is (may cause positioning issues but won't crash)
                abs_x = crop.x
                abs_y = crop.y
        
        return [
            Segment(
                Control.move_to(abs_x, abs_y).segment.text,
                style=_NULL_STYLE,
            ),
            Segment(sixel_data, style=_NULL_STYLE, control=((ControlType.CURSOR_FORWARD, 0),)),
            # Move cursor to end of rendered area to ensure proper positioning
            Segment(Control.move_to(abs_x + crop.width, abs_y + crop.height).segment.text, style=_NULL_STYLE),
        ]

    def _perform_generation(self) -> None:
        """Background task to generate sixel for the pending crop.

        This method is scheduled by a timer and does nothing if another more recent pending
        generation was queued in the meantime.
        """
        if not self._pending_generation:
            return

        # Capture and clear pending generation so concurrent calls will queue again
        crop, content_size, terminal_sizes = self._pending_generation
        self._pending_generation = None

        # Generate from scaled LRU if possible
        scaled_key = (id(self.image), content_size.width, content_size.height, terminal_sizes.width, terminal_sizes.height)
        if scaled_key in self._scaled_lru:
            image_data = self._scaled_lru[scaled_key]
        else:
            image_data = PixelData(self.image)
            image_data = self._scale_image(image_data, terminal_sizes)
            # store scaled LRU
            self._scaled_lru[scaled_key] = image_data
            while len(self._scaled_lru) > self._scaled_cache_size:
                self._scaled_lru.popitem(last=False)

        cropped = self._crop_image(image_data, crop, terminal_sizes)

        logger.debug("background: generating sixel for crop %s", crop)
        sixel_data = image_to_sixels(cropped.pil_image)

        sixel_key = (
            id(self.image),
            crop.x,
            crop.y,
            crop.width,
            crop.height,
            content_size.width,
            content_size.height,
            terminal_sizes.width,
            terminal_sizes.height,
        )
        self._sixel_lru[sixel_key] = sixel_data
        while len(self._sixel_lru) > self._sixel_cache_size:
            self._sixel_lru.popitem(last=False)

        # update quick-hit cache and request a refresh
        self._cached_sixels = _CachedSixels(self.image, crop, content_size, terminal_sizes, sixel_data)
        try:
            self.refresh()
        except Exception:
            # be defensive; refresh could fail if widget destroyed
            pass

    def _perform_full_pregen(self, scaled_key: Tuple, full_key: Tuple, scaled_image: PixelData) -> None:
        """Generate sixel for the entire scaled image and cache it.

        This helps the case where the full image becomes visible (no cropping) and avoids
        generating the large sixel on-demand when the user scrolls to that position.
        """
        try:
            logger.debug("full pregeneration: generating sixel for scaled image")
            sixel_data = image_to_sixels(scaled_image.pil_image)
            self._sixel_lru[full_key] = sixel_data
            while len(self._sixel_lru) > self._sixel_cache_size:
                self._sixel_lru.popitem(last=False)
            # no immediate refresh here; it will be used when requested
        except Exception:
            logger.exception("error during full pregeneration")
            return
