from chains.rag_chain import rag_chain
from chains.tool_chain import tool_chain


CHAIN_MAPPING = {

    "risk": tool_chain,

    "transactions": tool_chain,

    "screen": tool_chain,

    "velocity": tool_chain,

    "counterparty": tool_chain,

    "alerts": tool_chain,

    "typology": tool_chain,

    "edd": tool_chain,

    "jurisdiction": tool_chain,

    "str": tool_chain,

    "ubo": tool_chain,

    "summary": tool_chain,

    "timeline": tool_chain,

    "memo": tool_chain,

    "deadline": tool_chain,

    "investigation": tool_chain,

    "rag": rag_chain

}



def get_chain(intent):

    return CHAIN_MAPPING.get(

        intent,

        rag_chain

    )