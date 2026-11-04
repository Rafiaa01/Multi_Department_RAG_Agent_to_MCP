
from langchain.tools import tool

from src.rag.retriever.retrieval_tool import retrieve_documents
from src.rag.retriever.source_formatter import format_sources


def create_hr_tool(vector_store):

    @tool
    def search_hr_documents(query: str) -> str:
        """
        Search HR policies about annual leave, sick leave,
        attendance, employee benefits, holidays, and remote work.
        """

        try:
            documents = retrieve_documents(
                vector_store=vector_store,
                query=query,
            )

            if not documents:
                return "No relevant HR documents found."

            sources = format_sources(documents)

            context = "\n\n".join(
                doc.page_content for doc in documents
            )

            return (
                f"Retrieved HR evidence:\n{context}\n\n"
                f"Sources:\n" + "\n".join(sources)
            )

        except Exception as e:  # noqa: BLE001
            return "HR document search is temporarily unavailable.", str(e)

    return search_hr_documents
