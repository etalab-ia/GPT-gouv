import bs4
import pandas as pd
from typing import List
import numpy as np


def process_answers(df: pd.Series) -> pd.Series:
    def filter_one_answer(l: List[str]) -> List[str]:
        return [text for text in l \
                if "bonjour" not in text.lower() and "merci" not in text.lower() \
                    and "heureux" not in text.lower() and "le service public concerné" not in text.lower() \
                    and "nous sommes attaché" not in text.lower() \
                    and "particulièrement attaché" not in text.lower() \
                    and "gêne occasionnée" not in text.lower() \
                    and "souhaitons" not in text.lower() \
                    and "prenons note de votre témoignage" not in text.lower() \
                    and "le meilleur service à nos assurés" not in text.lower() \
                    and "bonne retraite" not in text.lower()

                ]

    def process_one_answer(row: str) -> str:
        soup = bs4.BeautifulSoup(row, "html.parser")
        answers = [a.text for a in soup.find_all(["p", "ul", "ol"])]
        return " ".join(
            filter_one_answer(answers)
        )

    return df.apply(lambda row: process_one_answer(row))


path = "../../data/raw/___liste_des_experiences_publiees_2023-05-09T14_25_40.084962Z.csv"

df = pd.read_csv(path, sep=",").drop_duplicates(subset=["ID"]).dropna(subset=["rep_administration"])

processed_answers = process_answers(df["rep_administration"])

#titles, comments, answers, processed_answers = df["titre"].values, df["expérience"].values

df_out = df[["créée_le","titre", "expérience", "typologie", "rep_administration"]]
df_out["processed_answers"] = processed_answers.replace('', np.nan)

df_out.dropna(subset=["processed_answers"]).to_csv("../../data/processed/processed_answers_spp.csv", sep="~", index=False)
#print(titles[:10], comments[:10], answers[:10])
