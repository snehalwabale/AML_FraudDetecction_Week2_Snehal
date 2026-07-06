from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from rag.query_transform import rewrite_query
from rag.reranker import rerank_documents

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)


def generate_answer(question: str,session_id: str):

    rewritten_query = rewrite_query(question)

    documents = rerank_documents(rewritten_query)

    context = "\n\n".join(

        doc.page_content

        for doc in documents

    )

    prompt = f"""
You are an AML & Fraud Detection Investigation Copilot.

Answer the investigator's question using the retrieved context.

If the answer is not present in the context,
say that the information is unavailable.

Retrieved Context

{context}

Question

{question}

Provide:
1. Investigation Summary
2. Risk Assessment
3. Recommended Action
"""

    response = llm.invoke(prompt)

    citations = []

    retrieval_trace = []

    for doc in documents:

        citations.append(

            {

                "doc_id": doc.metadata.get(

                    "doc_id",

                    "Unknown"

                ),

                "score": doc.metadata.get(

                    "score",

                    0

                )

            }

        )

        retrieval_trace.append(

            doc.metadata

        )

    return (

        response.content,

        citations,

        retrieval_trace

    )