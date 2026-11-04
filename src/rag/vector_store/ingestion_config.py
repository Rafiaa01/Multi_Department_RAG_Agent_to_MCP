from pathlib import Path

from langchain_openai import OpenAIEmbeddings

# Project directory: src/
BASE_DIR = Path(__file__).resolve().parents[2]

# Department PDF directories
DATA_DIR = BASE_DIR / "data"

# FAISS index directories
VECTOR_STORE_DIR = BASE_DIR / "vector_stores"

# Supported departments
DEPARTMENTS = ["hr", "it", "finance"]

# Embedding configuration
EMBEDDING_MODEL = "text-embedding-3-small"

# Reuse one embedding model instance
embeddings = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
)
