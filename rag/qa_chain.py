from dotenv import load_dotenv

from langchain_openai import ChatOpenAI


from rag.query_transform import rewrite_query

from rag.retriever_hybrid import hybrid_search


load_dotenv()



llm = ChatOpenAI(

    model="gpt-4o-mini",

    temperature=0.2

)



def generate_answer(

    question: str,

    role: str = "analyst"

):


    rewritten_query = rewrite_query(

        question

    )


    documents = hybrid_search(

        rewritten_query,

        role=role

    )


    context = "\n\n".join(

        doc.page_content

        for doc in documents

    )



    prompt=f"""

You are an AML & Fraud Detection Investigation Copilot.


User Role:

{role}



Use only authorized retrieved documents.


Context:

{context}



Question:

{question}



Provide:

1. Investigation Summary

2. Risk Assessment

3. Recommended Action


"""



    response = llm.invoke(

        prompt

    )



    citations=[]

    retrieval_trace=[]



    for doc in documents:


        citations.append({

            "doc_id":
            doc.metadata.get(
                "doc_id",
                "Unknown"
            )

        })


        retrieval_trace.append(

            doc.metadata

        )



    return (

        response.content,

        citations,

        retrieval_trace

    )