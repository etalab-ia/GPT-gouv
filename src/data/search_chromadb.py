import chromadb
import pandas as pd
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import os

chroma_client = chromadb.Client(
    Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=os.path.join("..", "..", "data", "processed")
    )
)

model_name = "all-MiniLM-L6-v2"
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=model_name
)
collection = chroma_client.get_or_create_collection(
    name=model_name, embedding_function=sentence_transformer_ef
)


results = collection.query(
    query_texts="Bonjour comment puis-je obtenir une nouvelle carte d'identité ?",
    n_results=5,
)
print(results)
