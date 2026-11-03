from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_and_split_pdf(pdf_path: str, department: str):

    # Load PDF pages
    pages = PyPDFLoader(pdf_path).load()

    if not pages:
        raise ValueError(f"No pages found in {pdf_path}")

    # Combine all pages and remember their character positions
    full_text = ""
    page_positions = []

    for page in pages:
        start = len(full_text)
        full_text += page.page_content + "\n"
        end = len(full_text)

        page_positions.append({
            "start": start,
            "end": end,
            "page": page.metadata["page"] + 1,
        })

    # Split combined text into overlapping chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        add_start_index=True,
    )

    chunks = splitter.create_documents([full_text])

    # Attach source and page metadata to each chunk
    result = []

    for chunk in chunks:
        start = chunk.metadata["start_index"]
        end = start + len(chunk.page_content)

        pages_used = [
            p["page"]
            for p in page_positions
            if p["start"] < end and p["end"] > start
        ]

        result.append(
            Document(
                page_content=chunk.page_content,
                metadata={
                    "source": Path(pdf_path).name,
                    "department": department,
                    "page_numbers": pages_used,
                },
            )
        )

    return result