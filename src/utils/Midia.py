import tkinter as tk
from tkinter import filedialog
import io
from enum import Enum


class Tipo(Enum):
    VIDEO = [
        ("Vídeos", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm"),
        ("Todos os arquivos", "*.*"),
    ]

    IMAGEM = [
        ("Imagens", "*.png *.jpg *.jpeg *.gif *.bmp *.webp *.tiff"),
        ("Todos os arquivos", "*.*"),
    ]

    DOCUMENTO = [
        ("Documentos", "*.pdf *.txt *.doc *.docx *.xls *.xlsx *.ppt *.pptx *.odt *.ods *.odp"),
        ("Todos os arquivos", "*.*"),
    ]

    AUDIO = [
        ("Áudio", "*.mp3 *.wav *.ogg *.flac *.aac *.m4a *.wma"),
        ("Todos os arquivos", "*.*"),
    ]


def selecionar_arquivo(tipo):
    root = tk.Tk()
    root.withdraw()

    caminhos = filedialog.askopenfilenames(
        title="Selecione",
        filetypes=tipo.value
    )

    root.destroy()
    return caminhos


def get_bytes(caminho):
    with open(caminho, "rb") as f:
        return f.read()


def get_io_bytes(caminho):
    with open(caminho, "rb") as f:
        blob = f.read()
    return io.BytesIO(blob)


if __name__ == "__main__":
    print(selecionar_arquivo())
