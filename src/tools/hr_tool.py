from langchain.tools import tool
from src.rag.retriever.retrieval_tool import retrieve_documents


def create_hr_tool(vector_store):

    @tool
    def search_hr_documents(query: str) -> str:
        """Search HR policies about annual leave, sick leave, attendance, employee benefits, holidays, and remote work."""

        try:
            documents = retrieve_documents(vector_store, query)

            if not documents:
                return "No relevant HR documents found."

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
            return f"HR search failed: {str(e)}"  # noqa: RUF010

    return search_hr_documents
