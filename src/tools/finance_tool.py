from langchain.tools import tool
from src.rag.retriever.retrieval_tool import retrieve_documents


def create_finance_tool(vector_store):

    @tool
    def search_finance_documents(query: str) -> str:
        """Search Finance policies about reimbursement,eligible expenses, travel allowances, expense claims,home office stipends, and payment limits."""

        try:
            documents = retrieve_documents(vector_store, query)

            if not documents:
                return "No relevant Finance documents found."

            results = []

            for doc in documents:
                results.append(
                    f"""
                    Source: {doc.metadata["source"]}
                    Pages: {doc.metadata["page_numbers"]}
                    Content: {doc.page_content}
                    """
                )

            return "\n\n".join(results)

        except Exception as e:  # noqa: BLE001
            return f"Finance search failed: {str(e)}"  # noqa: RUF010

    return search_finance_documents
