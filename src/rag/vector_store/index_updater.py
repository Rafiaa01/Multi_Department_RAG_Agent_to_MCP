from uuid import uuid4

from langchain_community.vectorstores import FAISS

from src.rag.chunks.chunking import load_and_split_pdf


def update_vector_store(
    vector_store: FAISS,
    department: str,
    files_to_add: dict,
    files_to_remove: dict,
):
    """Replace outdated chunks and add chunks from new or modified PDFs."""

    document_records = {}
    new_chunks = []
    new_chunk_ids = []

    # Prepare chunks from new or modified PDFs.
    for filename, file_info in files_to_add.items():
        chunks = load_and_split_pdf(
            pdf_path=str(file_info["path"]),
            department=department,
        )

        chunk_ids = []

        for chunk in chunks:
            chunk_id = str(uuid4())

            new_chunks.append(chunk)
            new_chunk_ids.append(chunk_id)
            chunk_ids.append(chunk_id)

        document_records[filename] = {
            "hash": file_info["hash"],
            "chunk_ids": chunk_ids,
        }

    # Add new chunks to the existing index.
    if new_chunks:
        vector_store.add_documents(
            documents=new_chunks,
            ids=new_chunk_ids,
        )

    # Collect IDs of outdated chunks.
    old_chunk_ids = [
        chunk_id
        for record in files_to_remove.values()
        for chunk_id in record.get("chunk_ids", [])
    ]

    # Remove outdated chunks from the index.
    if old_chunk_ids:
        vector_store.delete(ids=old_chunk_ids)

    return vector_store, document_records
