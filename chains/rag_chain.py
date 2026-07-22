from langchain_core.runnables import RunnableLambda

from rag.qa_chain import generate_answer

from chains.base import BaseChain



def rag_node(inputs):

    try:

        answer, citations, trace = generate_answer(

            inputs.get("question", ""),

            inputs.get("role", "analyst")

        )


        return {

            "tool_output": answer,

            "citations": citations,

            "trace": trace,

            "evidence": []

        }


    except Exception as e:


        return {

            "tool_output": {

                "error": str(e)

            },

            "citations": [],

            "trace": [

                {

                    "stage": "rag_failed",

                    "error": str(e)

                }

            ],

            "evidence": []

        }



rag_chain = BaseChain(

    RunnableLambda(rag_node)

)