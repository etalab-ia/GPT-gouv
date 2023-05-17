import chromadb
import pandas as pd
from chromadb.utils import embedding_functions

chroma_client = chromadb.Client()



sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
collection = chroma_client.get_or_create_collection(name="my_collection", embedding_function=sentence_transformer_ef)

answers = pd.read_csv("../../data/processed/processed_answers_spp.csv", sep="~")[["titre", "expérience", "processed_answers"]]
answers["question"] = answers["titre"] + " " + answers["expérience"]

n = 20
### ADD EMBEDDINGS
collection.add(
    documents=answers["question"].values[:n],
    metadatas=[{"answer": answer} for answer in answers["processed_answers"].values[:n]],
    ids=answers.index[:n]
)

results = collection.query(
    query_texts=answers["question"].values[0],
    n_results=5
)
print(results)
