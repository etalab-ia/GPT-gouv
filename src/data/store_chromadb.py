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

answers = pd.read_csv("../../data/processed/processed_answers_spp.csv", sep="~")[
    ["titre", "expérience", "typologie", "processed_answers"]
]
answers["question"] = answers["titre"] + " " + answers["expérience"]

n = -1
### ADD EMBEDDINGS
collection.add(
    documents=list(answers["question"].values[:n]),
    metadatas=[
        {"answer": answer, "typology": answers["typologie"].values[k], "title": answers["titre"].values[k]}
        for k, answer in enumerate(answers["processed_answers"].values[:n])
    ],
    ids=[str(id) for id in answers.index[:n].values],
)
