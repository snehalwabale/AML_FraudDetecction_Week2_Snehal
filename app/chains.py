from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from app.prompts import (
    prompt,
    get_examples
)

from app.models import (
    AMLResponse
)

from app.tools import *


try:

    from langsmith import traceable

except Exception:

    def traceable(func):
        return func


load_dotenv()


llm = ChatOpenAI(

    model="gpt-4o-mini",

    temperature=0.2
)


def run_tool(query):

    q = query.lower()

    if "analyze" in q:

        return (

            analyze_transactions(
                "55-389"
            ),

            "Transaction Analyzer"
        )

    elif "sar" in q:

        return (

            generate_sar(

                "55-389",

                "Structuring detected"
            ),

            "SAR Generator"
        )

    elif "screen" in q:

        return (

            screen_name(
                "Viktor Petrov"
            ),

            "Sanctions Screener"
        )

    elif "pep" in q:

        return (

            screen_name(
                "Viktor Petrov"
            ),

            "PEP Screener"
        )

    elif "risk score" in q:

        return (

            get_risk_score(
                "C-7781"
            ),

            "Risk Score Tool"
        )

    elif "velocity" in q:

        return (

            transaction_velocity(),

            "Velocity Analyzer"
        )

    elif "counterpart" in q:

        return (

            counterparties(),

            "Counterparty Tool"
        )

    elif "previous alert" in q:

        return (

            previous_alerts(),

            "Alert History Tool"
        )

    elif "typology" in q:

        return (

            typology(),

            "Typology Tool"
        )

    elif "deadline" in q:

        return (

            filing_deadline(),

            "Deadline Tool"
        )

    elif "due diligence" in q:

        return (

            enhanced_due_diligence(),

            "EDD Tool"
        )

    elif "jurisdiction" in q:

        return (

            jurisdiction_check(),

            "Jurisdiction Tool"
        )

    elif "str field" in q:

        return (

            str_fields(),

            "STR Tool"
        )

    elif "beneficial owner" in q:

        return (

            ultimate_beneficial_owner(),

            "UBO Tool"
        )

    elif "open aml alerts" in q:

        return (

            alert_summary(),

            "Alert Summary Tool"
        )

    elif "timeline" in q:

        return (

            investigation_timeline(),

            "Timeline Tool"
        )

    elif "memo" in q:

        return (

            escalation_memo(),

            "Escalation Memo Tool"
        )

    return (

        None,

        "No Tool"
    )


def fallback_response():

    return AMLResponse(

        response=
        "Unable to process request right now. Please try again.",

        risk_score=0,

        action="Retry",

        tool_used="Fallback"
    )


@traceable
def ask_llm(

    question,

    history

):

    try:

        tool_output, tool_name = run_tool(
            question
        )

        selected_examples = get_examples(
            question
        )

        chain = prompt | llm

        response = chain.invoke(

            {

                "history":
                history,

                "examples":
                selected_examples,

                "question":
                question,

                "tool_output":
                str(tool_output)
            }
        )

        risk_score = 0

        if isinstance(
            tool_output,
            dict
        ):

            risk_score = tool_output.get(
                "risk_score",
                0
            )

        return AMLResponse(

            response=
            response.content,

            risk_score=
            risk_score,

            action=
            "Review",

            tool_used=
            tool_name
        )

    except Exception as e:

        print(
            "CHAIN ERROR:",
            e
        )

        return fallback_response()