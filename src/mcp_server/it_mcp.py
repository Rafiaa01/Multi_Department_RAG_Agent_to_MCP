
from fastmcp import FastMCP

from src.rag.retriever.retrieval_tool import retrieve_documents
from src.rag.vector_store.ingestion_services import ingest_department

mcp = FastMCP("IT RAG Server")

# Initialize only the IT vector store
vector_store = ingest_department("it")


@mcp.tool()
def search_it_documents(query: str) -> str:
    """
    Search IT Support policies about password resets, laptop problems,
    technical support, IT equipment, and software access.
    """

    try:
        documents = retrieve_documents(vector_store, query)

        if not documents:
            return "No relevant IT documents found."

        results = []

        for doc in documents:
            results.append(
                f"""
Source: {doc.metadata.get("source", "Unknown")}
Pages: {doc.metadata.get("page_numbers", [])}
Content: {doc.page_content}
"""
            )

        return "\n\n".join(results)

    except Exception:  # noqa: BLE001
        return "IT document search is temporarily unavailable."


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8002,
    )
