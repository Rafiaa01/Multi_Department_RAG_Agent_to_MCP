from uuid import uuid4

from langchain_community.vectorstores import FAISS

from src.rag.chunks.chunking import load_and_split_pdf
from src.rag.vector_store.ingestion_config import embeddings


def build_department_index(department: str, pdf_files: dict):
    """Build a FAISS index using the department's PDF documents."""

    all_chunks = []
    document_records = {}

    for filename, file_info in pdf_files.items():
        chunks = load_and_split_pdf(
            pdf_path=str(file_info["path"]),
            department=department,
        )

        chunk_ids = []

        for chunk in chunks:
            chunk_id = str(uuid4())
            chunk_ids.append(chunk_id)
            all_chunks.append(chunk)

        document_records[filename] = {
            "hash": file_info["hash"],
            "chunk_ids": chunk_ids,
        }

    if not all_chunks:
        return None, document_records

    chunk_ids = [
        chunk_id
        for record in document_records.values()
        for chunk_id in record["chunk_ids"]
    ]

    vector_store = FAISS.from_documents(
        documents=all_chunks,
        embedding=embeddings,
        ids=chunk_ids,
    )

    return vector_store, document_records
