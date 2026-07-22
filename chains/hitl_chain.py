from chains.base import BaseChain

from langchain_core.runnables import RunnableLambda


def hitl_node(inputs):

    return {

        "approved": True,

        "comments": "No HITL Required"

    }


hitl_chain = BaseChain(

    RunnableLambda(hitl_node)

)