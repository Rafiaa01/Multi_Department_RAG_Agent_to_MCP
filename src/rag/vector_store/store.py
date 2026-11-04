from src.rag.vector_store.ingestion_config import DEPARTMENTS
from src.rag.vector_store.ingestion_services import ingest_department


def create_all_vector_stores():
    """Create or incrementally update all department vector stores."""

    vector_stores = {}

    for department in DEPARTMENTS:
        vector_stores[department] = ingest_department(department)

    return vector_stores
