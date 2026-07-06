from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from app.models import AMLResponse
from app.memory import get_history
from app.prompts import prompt

from app.tools import (
    analyze_transactions,
    screen_name,
    get_risk_score,
    transaction_velocity,
    counterparties,
    previous_alerts,
    typology,
    filing_deadline,
    enhanced_due_diligence,
    jurisdiction_check,
    str_fields,
    ultimate_beneficial_owner,
    alert_summary,
    investigation_timeline,
    escalation_memo
)

from rag.qa_chain import generate_answer

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)


def route_query(query: str):

    q = query.lower()

    if any(x in q for x in [
        "risk",
        "score"
    ]):
        return "risk"

    if any(x in q for x in [
        "sanction",
        "ofac",
        "pep",
        "screen"
    ]):
        return "screen"

    if any(x in q for x in [
        "transaction",
        "transactions"
    ]):
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


def run_chat(query: str, session_id: str):

    history = get_history(session_id)

    intent = route_query(query)

    citations = []

    trace = []

    tool_used = "RAG"

    if intent == "risk":
        tool_output = str(get_risk_score())
        tool_used = "Risk Tool"

    elif intent == "screen":
        tool_output = str(screen_name())
        tool_used = "Sanction Tool"

    elif intent == "transactions":
        tool_output = str(analyze_transactions())
        tool_used = "Transaction Tool"

    elif intent == "velocity":
        tool_output = str(transaction_velocity())
        tool_used = "Velocity Tool"

    elif intent == "counterparty":
        tool_output = str(counterparties())
        tool_used = "Counterparty Tool"

    elif intent == "alerts":
        tool_output = str(previous_alerts())
        tool_used = "Alerts Tool"

    elif intent == "typology":
        tool_output = str(typology())
        tool_used = "Typology Tool"

    elif intent == "deadline":
        tool_output = str(filing_deadline())
        tool_used = "Deadline Tool"

    elif intent == "edd":
        tool_output = str(enhanced_due_diligence())
        tool_used = "EDD Tool"

    elif intent == "jurisdiction":
        tool_output = str(jurisdiction_check())
        tool_used = "Jurisdiction Tool"

    elif intent == "str":
        tool_output = str(str_fields())
        tool_used = "STR Tool"

    elif intent == "ubo":
        tool_output = str(ultimate_beneficial_owner())
        tool_used = "UBO Tool"

    elif intent == "summary":
        tool_output = str(alert_summary())
        tool_used = "Summary Tool"

    elif intent == "timeline":
        tool_output = str(investigation_timeline())
        tool_used = "Timeline Tool"

    elif intent == "memo":
        tool_output = escalation_memo()
        tool_used = "Memo Tool"

    else:
        tool_output, citations, trace = generate_answer(
            query,
            session_id
        )

    chain = prompt | llm

    response = chain.invoke(

        {

            "history": history,

            "examples": "",

            "tool_output": tool_output,

            "question": query

        }

    )

    return AMLResponse(

        response=response.content,

        risk_score=0,

        action="Completed",

        tool_used=tool_used,

        citations=citations,

        retrieval_trace=trace

    )


def run_retrieve(query, top_k=5):

    from rag.retriever_hybrid import hybrid_search

    return hybrid_search(query)[:top_k]