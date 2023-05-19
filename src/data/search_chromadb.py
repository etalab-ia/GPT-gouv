import chromadb
import pandas as pd
from chromadb.utils import embedding_functions
from chromadb.config import Settings
chroma_client = chromadb.Client(
    Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="../../data/processed" # Optional, defaults to .chromadb/ in the current directory
    )
)


sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="my_collection", embedding_function=sentence_transformer_ef)


results = collection.query(
    query_texts="Bonjour je paye trop d'impôts",
    n_results=5
)
print(results)
