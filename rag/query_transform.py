from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)


def rewrite_query(query: str):

    prompt = f"""
You are an AML investigation assistant.

Rewrite the following user query to improve document retrieval.

Rules:
- Preserve the original meaning.
- Expand abbreviations if appropriate.
- Include AML and Fraud terminology where relevant.
- Return only the rewritten query.

Query:
{query}
"""

    try:

        response = llm.invoke(prompt)

        return response.content.strip()

    except Exception:

        return query