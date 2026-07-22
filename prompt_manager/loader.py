import os
import json

from langchain_core.prompts import ChatPromptTemplate


PROMPT_DIR = "prompts"

REGISTRY_FILE = "data/prompt_registry.json"


DEFAULT_PROMPTS = {


    "rag_qa":

    """
You are an AML Fraud Detection Co-Pilot.

Role:
{role}

Domain:
{domain}

Use the provided context to answer.

Context:
{context}

Question:
{question}

Chat History:
{chat_history}

Rules:

- Do not hallucinate.
- Explain AML reasoning clearly.
- Mention risk indicators.
- Provide analyst recommendations.
""",



    "risk_analysis":

    """
You are an AML risk analyst.

Analyze the customer or transaction.

Input:

{question}


Provide:

1. Risk Score
2. Risk Level
3. Risk Indicators
4. Recommended Action


Context:

{context}
""",



    "sanction_screening":

    """
You are a sanctions screening assistant.

Analyze:

{question}


Provide:

- Match status
- PEP status
- Risk level
- Required action


Context:

{context}
""",



    "str_generation":

    """
Generate Suspicious Transaction Report assistance.


Input:

{question}


Create:


Subject:

Activity:

Risk Indicators:

Narrative:

Recommendation:
"""
}





def ensure_prompt_directory():

    if not os.path.exists(PROMPT_DIR):

        os.makedirs(PROMPT_DIR)




def load_registry():

    if not os.path.exists(REGISTRY_FILE):

        return {}


    with open(
        REGISTRY_FILE,
        "r"
    ) as file:

        return json.load(file)





def get_prompt_text(prompt_name:str):

    """
    Load raw prompt text.
    """


    ensure_prompt_directory()


    registry = load_registry()



    if prompt_name in registry:


        active_version = registry[prompt_name].get(
            "active_version"
        )


        if active_version:


            file_path = os.path.join(

                PROMPT_DIR,

                f"{prompt_name}_{active_version}.txt"

            )


            if os.path.exists(file_path):


                with open(
                    file_path,
                    "r"
                ) as file:

                    return file.read()



    normal_file = os.path.join(

        PROMPT_DIR,

        f"{prompt_name}.txt"

    )



    if os.path.exists(normal_file):


        with open(
            normal_file,
            "r"
        ) as file:

            return file.read()



    return DEFAULT_PROMPTS.get(

        prompt_name,

        DEFAULT_PROMPTS["rag_qa"]

    )





def load_prompt(prompt_name:str):

    """
    Returns LangChain ChatPromptTemplate.
    """

    prompt_text = get_prompt_text(
        prompt_name
    )


    return ChatPromptTemplate.from_template(

        prompt_text

    )