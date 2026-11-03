from langchain.tools import tool
from src.rag.retriever.retrieval_tool import retrieve_documents


def create_it_tool(vector_store):

    @tool
    def search_it_documents(query: str) -> str:
        """Search IT Support policies about password resets,laptop problems, technical support, IT equipment,software access, and hardware requests."""

        try:
            documents = retrieve_documents(vector_store, query)

            if not documents:
                return "No relevant IT documents found."

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
            return f"IT search failed: {str(e)}"  # noqa: RUF010

    return search_it_documents
