from pathlib import Path

from langchain_community.document_loaders import PyPDFDirectoryLoader

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"


def load_department_documents(department: str):

    department_path = DATA_DIR / department

    if not department_path.exists():
        raise FileNotFoundError(
            f"Department folder not found: {department_path}"
        )

    loader = PyPDFDirectoryLoader(str(department_path))

    documents = loader.load()

    for document in documents:
        document.metadata["department"] = department
        document.metadata["doc_name"] = Path(
            document.metadata["source"]
        ).name

        # PyPDFDirectoryLoader normally uses zero-based page numbers.
        document.metadata["page_number"] = (
            document.metadata.get("page", 0) + 1
        )

    return documents


def load_all_documents():

    departments = ["hr", "it", "finance"]

    all_documents = []

    for department in departments:
        documents = load_department_documents(department)
        all_documents.extend(documents)

    return all_documents