from typing import List, Dict


def get_prompt_instruction(responses_list: List[Dict[str, str]]) -> str:
    """
    Given a list of possible input (list of dicts with fields "answer" and "title"), generate a prompt to send to a LLM

    Args:
        responses_list (List[Dict[str, str]])
    Returns:
        str: the prompt
    """
    PROMPT_INSTRUCTION = f"### Résume moi les {len(responses_list)} textes suivants dans un seul texte court."
    for index, response in enumerate(responses_list):
        title = response["title"]
        PROMPT_INSTRUCTION += f"Le texte {index+1} parle de '{title}.'"
    for index, response in enumerate(responses_list):
        answer = response["answer"]
        PROMPT_INSTRUCTION += f"### Texte {index+1}: {answer} \n"
    PROMPT_INSTRUCTION += "### Résumé :"
    return PROMPT_INSTRUCTION
