
from langchain.tools import tool

from src.rag.retriever.retrieval_tool import retrieve_documents
from src.rag.retriever.source_formatter import format_sources


def create_it_tool(vector_store):

    @tool
    def search_it_documents(query: str) -> str:
        """
        Search IT Support policies about password resets,
        laptop problems, technical support, IT equipment,
        software access, and hardware requests.
        """

        try:
            documents = retrieve_documents(
                vector_store=vector_store,
                query=query,
            )

            if not documents:
                return "No relevant IT documents found."

            sources = format_sources(documents)

            context = "\n\n".join(
                doc.page_content for doc in documents
            )

            return (
                f"Retrieved IT evidence:\n{context}\n\n"
                f"Sources:\n" + "\n".join(sources)
            )

        except Exception as e:   # noqa: BLE001
            return "IT document search is temporarily unavailable.", str(e)

    return search_it_documents
