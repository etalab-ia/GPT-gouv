import pandas as pd
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
import os
from typing import Dict, List
from prompt_for_summary import get_prompt_instruction
import requests as r
from src.models.credentials import access_token


def add_greetings(df: pd.Series) -> pd.DataFrame:
    """
    Add greetings to the beginnings of the answers.

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    return df


def add_closing_remarks(df: pd.Series) -> pd.DataFrame:
    """
    Add closing remarks to the end of the answers.

    Args:
        df (pd.DataFrame): _description_

    Returns:
        pd.DataFrame: _description_
    """
    return df


def filter_reponse_typology(query_response: Dict, input_typologies: List[str]) -> Dict:
    """
    Filter query response on typology.
    TO BE COMPLETED and evaluated

    Args:
        query_response (Dict): _description_
        input_typologies (List[str]): _description_

    Returns:
        Dict: _description_
    """
    return query_response


def llm_query_huggingface(prompt: str, model_name: str) -> str:
    """
    Args:
        prompt (str) : prompt to send to the LLM
        model_name (str) : name of the model in huggingface API hub

    Returns:
        str: the output of the LLM
    """
    wait_for_model = model_name != "google/flan-t5-xxl"
    API_URL = f"https://api-inference.huggingface.co/models/{model_name}"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {"inputs": prompt, "options": {"use_cache": False, "wait_for_model": wait_for_model}}
    response = r.post(API_URL, headers=headers, json=payload)
    if model_name == "google/flan-t5-xxl":
        return response.json()[0]["generated_text"]
    else:
        # TODO: to customize according to the chosen model
        return response.json()


def get_llm_combination(responses: List[Dict[str, str]]) -> str:
    """
    Given a list of possible responses (dict with fields "answer" and "title"), summarize it into a single one

    Returns:
        str: the summarized answer of the LLM
    """
    prompt = get_prompt_instruction(responses)
    return llm_query_huggingface(prompt, model_name="google/flan-t5-xxl")

def generate_body(df: pd.DataFrame, model_name: str) -> pd.DataFrame:
    """
    Given a dataframe of questions including a column "question" and a column "typology",
    generate the body of the answers, with the key information for the citizens.

    Args:
        df (pd.DataFrame): dataframe with fields "question", "typology"

    Returns:
        pd.DataFrame: _description_
    """
    assert (
        "question" in df.columns and "typology" in df.columns
    ), "The columns 'question' and 'typology' are required"
    persist_dir = os.path.join("..", "..", "data", "processed")
    chroma_client = chromadb.Client(
        Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir)
    )

    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=model_name
    )
    collection = chroma_client.get_or_create_collection(
        name=model_name, embedding_function=sentence_transformer_ef
    )
    # filter response on tyopology basis
    # TODO : need to evaluate the relevance of this filter ??
    results = filter_reponse_typology(
        collection.query(query_texts=df["question"].values, n_results=3),
        input_typologies=df["typology"].values,
    )
    possible_answers = [
        get_llm_combination(candidates_dict) for candidates_dict in results["metadatas"]
    ]
    df["answer"] = possible_answers
    return df


def generate_answers(
    df: pd.DataFrame, model_name: str = "all-MiniLM-L6-v2"
) -> pd.DataFrame:
    """
    Generate naive answers based on a dataframe of questions

    Args:
        df (pd.DataFrame): dataframe with fields "question", "typology"
        model_name (str, optional): the name of the embeddings model to use. Defaults to "all-MiniLM-L6-v2".

    Returns:
        pd.DataFrame: dataframe with fields "question", "typology" and now a field "answer"
    """
    df = generate_body(df, model_name=model_name)
    df["answer"] = add_closing_remarks(add_greetings(df["answer"]))
    return df


if __name__ == "__main__":
    df = pd.DataFrame(
        data={
            "question": [
                "Bonjour comment puis-je obtenir une nouvelle carte d'identité ?"
            ],
            "typology": ["ANTS"],
        }
    )
    print(df)
    answers = generate_answers(df)
    print(answers)
