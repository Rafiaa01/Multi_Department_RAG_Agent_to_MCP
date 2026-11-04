
from langchain.tools import tool

from src.rag.retriever.retrieval_tool import retrieve_documents
from src.rag.retriever.source_formatter import format_sources


def create_finance_tool(vector_store):

    @tool
    def search_finance_documents(query: str) -> str:
        """
        Search Finance policies about reimbursement,
        eligible expenses, travel allowances, expense claims,
        home office stipends, and payment limits.
        """

        try:
            documents = retrieve_documents(
                vector_store=vector_store,
                query=query,
            )

            if not documents:
                return "No relevant Finance documents found."

            sources = format_sources(documents)

            context = "\n\n".join(
                doc.page_content for doc in documents
            )

            return (
                f"Retrieved Finance evidence:\n{context}\n\n"
                f"Sources:\n" + "\n".join(sources)
            )

        except Exception as e:  # noqa: BLE001
            return "Finance document search is temporarily unavailable.", str(e)

    return search_finance_documents
