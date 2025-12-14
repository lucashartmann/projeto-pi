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
    ) -> None:
        super().__init__(name=name, id=id, classes=classes)
        assert protocol in ["Auto", "TGP", "Sixel", "Halfcell", "Unicode", ""]
        self.protocol = protocol
        self.path = path
        self.use_keys = use_keys
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

        elif self.doc_type == "txt":
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
        width, height = 900, max(300, len(lines) * 20 + 40)
        image = PILImage.new("RGB", (width, height), "white")
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()

        # Define the maximum width for text (accounting for margins)
        max_text_width = width - 20  # 10 pixels margin on each side

        y = 10
        for line in lines:
            # Wrap the text to fit within the image width
            # Adjust width based on font size
            wrapped_lines = textwrap.wrap(line, width=80)
            for wrapped_line in wrapped_lines:
                draw.text((10, y), wrapped_line, fill="black", font=font)
                y += 18  # Adjust line spacing
            if not wrapped_lines:  # Handle empty lines
                y += 18
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
