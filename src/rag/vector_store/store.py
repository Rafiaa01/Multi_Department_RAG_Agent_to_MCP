from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from src.rag.chunks.chunking import load_and_split_pdf

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
VECTOR_STORE_DIR = BASE_DIR / "vector_stores"


def create_department_vector_store(department: str):

    department_path = DATA_DIR / department
    pdf_files = list(department_path.glob("*.pdf"))

    if not pdf_files:
        raise ValueError(f"No PDF files found for {department}")

    all_chunks = []

    for pdf_file in pdf_files:
        chunks = load_and_split_pdf(
            pdf_path=str(pdf_file),
            department=department,
        )
        all_chunks.extend(chunks)

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = FAISS.from_documents(
        documents=all_chunks,
        embedding=embeddings,
    )

    save_path = VECTOR_STORE_DIR / department
    save_path.mkdir(parents=True, exist_ok=True)

    vector_store.save_local(str(save_path))

    return vector_store


def create_all_vector_stores():

    vector_stores = {}

    for department in ["hr", "it", "finance"]:
        vector_stores[department] = create_department_vector_store(department)

    return vector_stores
