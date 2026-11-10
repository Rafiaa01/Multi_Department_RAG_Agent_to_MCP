
from fastmcp import FastMCP

from src.rag.retriever.retrieval_tool import retrieve_documents
from src.rag.vector_store.ingestion_services import ingest_department
from src.tools.safe_calculator_tool import calculate

mcp = FastMCP("Finance RAG Server")

# Initialize only the Finance vector store
vector_store = ingest_department("finance")


@mcp.tool()
def search_finance_documents(query: str) -> str:
    """
    Search Finance policies about reimbursement, eligible expenses,
    travel allowances, expense claims, and payment limits.
    """

    try:
        documents = retrieve_documents(vector_store, query)

        if not documents:
            return "No relevant Finance documents found."

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
        return "Finance document search is temporarily unavailable."

@mcp.tool()
def calculator(expression: str) -> str:
    """
    Perform safe arithmetic calculations using numbers and
    operators such as +, -, *, /, %, and **.
    """

    try:
        result = calculate(expression)
        return str(result)

    except Exception as e:  # noqa: BLE001
        return f"Calculation error: {str(e)}"  # noqa: RUF010
    
if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8003,
    )
