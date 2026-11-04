
import logging

logger = logging.getLogger(__name__)


def retrieve_documents(
    vector_store,
    query: str,
    k: int = 5,
    threshold: float = 0.15,
):
    try:
        results = vector_store.similarity_search_with_relevance_scores(
            query=query,
            k=k,
        )

        relevant_documents = [
            document
            for document, score in results
            if score >= threshold
        ]

        logger.info(
            "Retrieved %d relevant documents for query: %s",
            len(relevant_documents),
            query,
        )

        return relevant_documents

    except Exception:
        logger.exception("Document retrieval failed")
        raise
