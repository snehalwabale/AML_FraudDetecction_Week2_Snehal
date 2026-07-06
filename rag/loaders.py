from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
    Docx2txtLoader,
    UnstructuredHTMLLoader
)


def load_document(file_path: str):

    path = Path(file_path)

    suffix = path.suffix.lower()

    if suffix == ".pdf":
        loader = PyPDFLoader(file_path)

    elif suffix == ".docx":
        loader = Docx2txtLoader(file_path)

    elif suffix == ".csv":
        loader = CSVLoader(file_path)

    elif suffix in [".html", ".htm"]:
        loader = UnstructuredHTMLLoader(file_path)

    else:
        loader = TextLoader(
            file_path,
            encoding="utf-8"
        )

    return loader.load()