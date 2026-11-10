from fastmcp import FastMCP

from src.rag.retriever.retrieval_tool import retrieve_documents
from src.rag.vector_store.store import create_all_vector_stores

mcp = FastMCP("HR RAG Server")

# Initialize the existing HR vector store
vector_store = create_all_vector_stores().get("hr")


@mcp.tool()
def search_hr_documents(query: str) -> str:
    """
    Search HR policies about annual leave, sick leave, attendance,
    employee benefits, holidays, and remote work.
    """

    try:
        documents = retrieve_documents(vector_store, query)

        if not documents:
            return "No relevant HR documents found."

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
        return "HR document search is temporarily unavailable."


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8001,
    )
