from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from app.models import AMLResponse
from app.memory import get_history

from chains.router import get_chain

from prompt_manager.loader import load_prompt

from hitl.triggers import should_trigger_hitl
from hitl.manager import create_hitl_task


load_dotenv()


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)



def route_query(query: str):

    q = query.lower()


    if any(x in q for x in [
        "investigate",
        "investigation",
        "customer analysis",
        "full analysis",
        "complete review"
    ]):
        return "investigation"


    if any(x in q for x in [
        "risk",
        "score"
    ]):
        return "risk"


    if any(x in q for x in [
        "sanction",
        "pep",
        "ofac",
        "screen"
    ]):
        return "screen"


    if "transaction" in q:
        return "transactions"


    if "velocity" in q:
        return "velocity"


    if "counterparty" in q:
        return "counterparty"


    if "previous alert" in q:
        return "alerts"


    if "typology" in q:
        return "typology"


    if "deadline" in q:
        return "deadline"


    if "edd" in q:
        return "edd"


    if "jurisdiction" in q:
        return "jurisdiction"


    if "str" in q:
        return "str"


    if "ubo" in q:
        return "ubo"


    if "summary" in q:
        return "summary"


    if "timeline" in q:
        return "timeline"


    if "memo" in q:
        return "memo"


    return "rag"





def calculate_risk_score(intent, query):

    score = 0

    indicators = []


    keywords = {

        "fraud":15,
        "money laundering":20,
        "sanction":25,
        "pep":20,
        "terror":30,
        "freeze":20,
        "suspicious":15,
        "str":25,
        "sar":25

    }


    q = query.lower()


    for word,value in keywords.items():

        if word in q:

            score += value

            indicators.append(word)



    if intent in [
        "screen",
        "str",
        "typology",
        "investigation"
    ]:

        score += 30



    if intent in [
        "risk",
        "transactions",
        "investigation"
    ]:

        score += 20



    return min(score,100), indicators





def get_risk_level(score):

    if score >= 70:

        return "HIGH"


    if score >= 30:

        return "MEDIUM"


    return "LOW"






def run_chat(
    query:str,
    session_id:str,
    role:str="analyst"
):


    history = get_history(session_id)


    intent = route_query(query)


    risk_score, indicators = calculate_risk_score(
        intent,
        query
    )


    risk_level = get_risk_level(
        risk_score
    )


    try:

        trigger, reason = should_trigger_hitl(query)


        if trigger:


            task = create_hitl_task(

                query=query,

                recommendation="Human Approval Required",

                reason=reason

            )


            return AMLResponse(

                response=(

                    "Human approval required.\n\n"

                    f"Task ID: {task['task_id']}"

                ),

                risk_score=risk_score,

                risk_level=risk_level,

                action="Pending Approval",

                tool_used="HITL",

                intent=intent,

                recommendation="Manual compliance review",

                decision="Pending",

                evidence=[

                    {
                        "indicator":x
                    }

                    for x in indicators

                ]

            )


    except Exception:

        pass




    chain = get_chain(intent)



    result = chain.invoke(

        {

            "question":query,

            "intent":intent,

            "role":role

        }

    )



    tool_output = result.get(

        "tool_output",

        ""

    )


    citations = result.get(

        "citations",

        []

    )


    trace = result.get(

        "trace",

        []

    )


    evidence = result.get(

        "evidence",

        []

    )



    prompt_template = load_prompt(
        "rag_qa"
    )



    final_chain = prompt_template | llm



    response = final_chain.invoke(

        {

            "context":str(tool_output),

            "question":query,

            "role":role,

            "chat_history":history,

            "domain":"AML & Fraud Detection"

        }

    )



    return AMLResponse(

        response=response.content,

        risk_score=risk_score,

        risk_level=risk_level,

        action=(

            "Manual Investigation Required"

            if risk_level=="HIGH"

            else

            "Continue Monitoring"

        ),

        tool_used=intent.upper(),

        intent=intent,

        recommendation=(

            "Investigate customer activity"

            if risk_score >= 40

            else

            "Normal monitoring"

        ),

        decision="Completed",

        evidence=(

            evidence

            if evidence

            else

            [

                {

                    "risk_indicator":x

                }

                for x in indicators

            ]

        ),

        citations=citations,

        retrieval_trace=trace

    )







def run_retrieve(
    query,
    top_k=5,
    role="analyst"
):


    from rag.retriever_hybrid import hybrid_search


    return hybrid_search(

        query=query,

        top_k=top_k,

        role=role

    )