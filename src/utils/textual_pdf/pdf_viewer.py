import io
import mimetypes
from pathlib import Path
import fitz
import textual_image.widget as timg
from PIL import Image as PILImage, ImageDraw, ImageFont
from pymupdf import EmptyFileError, FileDataError
from textual import events
from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from docx import Document
from markdown import markdown
from bs4 import BeautifulSoup
import textwrap

from utils.textual_pdf.exceptions import NotAPDFError, PDFHasAPasswordError, PDFRuntimeError


class PDFViewer(Container):
    """Visualizador universal: PDF, DOCX, TXT e MD."""

    DEFAULT_CSS = """
    PDFViewer {
        height: 1fr;
        width: 1fr;
        Image {
            width: auto;
            height: auto;
            align: center bottom;
        }
    }
    """

    current_page: reactive[int] = reactive(0)
    protocol: reactive[str] = reactive("Auto")
    path: reactive[str | Path] = reactive("")
    total_pages: reactive[int] = reactive(1)

    def __init__(
        self,
        path: str | Path,
        protocol: str = "",
        use_keys: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        font_path: str | None = None,
        font_size: int = 10,
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        assert protocol in ["Auto", "TGP", "Sixel", "Halfcell", "Unicode", ""]
        self.protocol = protocol
        self.path = path
        self.use_keys = use_keys
        self.font_path = font_path
        self.font_size = font_size
        self.doc = None
        self.doc_type = None
        self.pages_cache = []
        self._check_file(path)

    def _guess_type(self, path) -> str:
        if isinstance(path, io.BytesIO):
            header = path.getvalue()[:4]
            if header.startswith(b"%PDF"):
                return "pdf"
            elif str(header).startswith("b'PK"):
                return "msword"
            else:
                return "txt"

        path = Path(path)
        guess, _ = mimetypes.guess_type(path)
        print(guess)
        if not guess:
            return "txt"
        return guess.split("/")[-1]

    def _check_file(self, path):
        file_type = self._guess_type(path)
        self.doc_type = file_type
        print(self.doc_type)

        if file_type == "pdf":
            try:
                self.doc = fitz.open(stream=path.getvalue(), filetype="pdf") if isinstance(
                    path, io.BytesIO) else fitz.open(path)
                if self.doc.is_encrypted and self.doc.needs_pass:
                    raise PDFHasAPasswordError(
                        f"{path} é protegido por senha.")
                self.total_pages = self.doc.page_count
            except (FileDataError, EmptyFileError):
                raise NotAPDFError(f"{path} não é um PDF válido.")

        elif file_type in ("plain", "txt"):
            text = path.getvalue().decode(errors="ignore") if isinstance(
                path, io.BytesIO) else Path(path).read_text(encoding="utf-8", errors="ignore")
            self.doc = text.splitlines()
            self.total_pages = max(1, len(self.doc) // 40 + 1)

        elif file_type in ("msword", "vnd.openxmlformats-officedocument.wordprocessingml.document"):
            doc = Document(path)
            # Extract all paragraphs and wrap them to estimate lines
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            wrapped_lines = []
            for p in paragraphs:
                # Wrap at 80 characters
                wrapped_lines.extend(textwrap.wrap(p, width=80))
            self.doc = wrapped_lines
            # Estimate pages based on wrapped lines
            self.total_pages = max(1, len(wrapped_lines) // 30 + 1)

        elif file_type in ("markdown", "md"):
            text = path.getvalue().decode(errors="ignore") if isinstance(
                path, io.BytesIO) else Path(path).read_text(encoding="utf-8", errors="ignore")
            self.doc = self._split_markdown_pages(text)
            self.total_pages = len(self.doc)

        else:
            raise NotAPDFError(f"Formato não suportado: {file_type}")

    def _split_markdown_pages(self, text: str):
        """Divide markdown em páginas com base em títulos e tamanho."""
        html = markdown(text)
        soup = BeautifulSoup(html, "html.parser")

        pages = []
        buffer = ""
        count = 0

        for element in soup.descendants:
            if element.name in ("h1", "h2", "h3") or (isinstance(element, str) and len(buffer) > 1500):
                if buffer.strip():
                    pages.append(buffer.strip())
                    buffer = ""
                if element.name in ("h1", "h2", "h3"):
                    buffer += f"# {element.text}\n\n"
            elif isinstance(element, str):
                buffer += element.strip() + " "

        if buffer.strip():
            pages.append(buffer.strip())

        return pages or ["(vazio)"]

    def on_mount(self):
        self.render_page()
        self.can_focus = True

    def compose(self) -> ComposeResult:
        yield timg.__dict__["Image"](PILImage.new("RGB", (800, 600), "white"), id="pdf-image")

    def _render_page_pil(self, page_index: int):
        if self.doc_type == "pdf":
            page = self.doc.load_page(page_index)
            pix = page.get_pixmap()
            mode = "RGBA" if pix.alpha else "RGB"
            return PILImage.frombytes(mode, (pix.width, pix.height), pix.samples)

        elif self.doc_type in ("txt", "plain"):
            lines = self.doc[page_index * 40:(page_index + 1) * 40]
            return self._draw_text_page(lines)

        elif self.doc_type in ("msword", "vnd.openxmlformats-officedocument.wordprocessingml.document"):
            lines = self.doc[page_index * 30:(page_index + 1) * 30]
            return self._draw_text_page(lines)

        elif self.doc_type in ("markdown", "md"):
            text = self.doc[page_index]
            lines = text.splitlines()
            return self._draw_text_page(lines)

        else:
            raise PDFRuntimeError(f"Tipo desconhecido: {self.doc_type}")

    def _draw_text_page(self, lines):
        width = 900

        # Try to load a TTF font at the requested size; fall back gracefully
        try:
            if getattr(self, 'font_path', None):
                font = ImageFont.truetype(self.font_path, self.font_size)
            else:
                font = ImageFont.truetype("arial.ttf", self.font_size)
        except Exception:
            try:
                font = ImageFont.truetype("DejaVuSans.ttf", self.font_size)
            except Exception:
                font = ImageFont.load_default()

        # Define a helper that wraps text by pixel width
        def wrap_text_by_pixel(draw_obj, text, font_obj, max_width):
            if not text:
                return [""]
            words = text.split()
            lines_out = []
            line = words[0]
            for w in words[1:]:
                test = line + " " + w
                try:
                    bbox = draw_obj.textbbox((0, 0), test, font=font_obj)
                    test_width = bbox[2] - bbox[0]
                except Exception:
                    test_width = draw_obj.textlength(test, font=font_obj) if hasattr(draw_obj, "textlength") else len(test) * (self.font_size // 2)
                if test_width <= max_width:
                    line = test
                else:
                    lines_out.append(line)
                    line = w
            lines_out.append(line)
            return lines_out

        # temporary image to measure wrapped lines
        temp_img = PILImage.new("RGB", (width, 2000), "white")
        temp_draw = ImageDraw.Draw(temp_img)
        max_text_width = width - 20

        est_lines = 0
        for line in lines:
            wrapped = wrap_text_by_pixel(temp_draw, line, font, max_text_width)
            est_lines += max(1, len(wrapped))

        try:
            ascent, descent = font.getmetrics()
            line_height = ascent + descent + 4
        except Exception:
            line_height = self.font_size + 6

        height = max(300, est_lines * line_height + 40)

        image = PILImage.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)

        y = 10
        for line in lines:
            wrapped = wrap_text_by_pixel(draw, line, font, max_text_width)
            for wrapped_line in wrapped:
                draw.text((10, y), wrapped_line, fill="black", font=font)
                y += line_height
            if wrapped == [""]:
                y += 6

        final_height = max(300, y + 10)
        if final_height != height:
            image = image.crop((0, 0, width, final_height))
        return image

    def render_page(self):
        if not self.doc:
            raise PDFRuntimeError("Nenhum documento aberto.")
        image_widget: timg.Image = self.query_one("#pdf-image")
        image_widget.image = self._render_page_pil(self.current_page)

    def on_key(self, event: events.Key):
        if not self.use_keys:
            return
        match event.key:
            case "down" | "page_down" | "right":
                event.stop()
                self.next_page()
            case "up" | "page_up" | "left":
                event.stop()
                self.previous_page()
            case "home":
                self.go_to_start()
            case "end":
                self.go_to_end()
                
    def load(self, path: str | Path | io.BytesIO, reset_page: bool = True):
        print(path)
        try:
            self.path = path
            self._check_file(path)
            if reset_page:
                self.current_page = 0
            
            self.render_page()
        except Exception as e:
                print("ERRO!", e)
                pass

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.render_page()

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.render_page()

    def go_to_start(self):
        self.current_page = 0
        self.render_page()

    def go_to_end(self):
        self.current_page = self.total_pages - 1
        self.render_page()
