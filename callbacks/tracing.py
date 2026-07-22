import os

from langchain_core.tracers import LangChainTracer


def get_langsmith_tracer():

    if os.getenv(
        "LANGCHAIN_TRACING_V2"
    ) == "true":

        return LangChainTracer(

            project_name=os.getenv(

                "LANGCHAIN_PROJECT",

                "AML-Fraud-Copilot"

            )

        )


    return None



def tracing_config(
    session_id: str,
    user_role: str
):

    tracer = get_langsmith_tracer()


    config = {

        "metadata":

        {

            "session_id":
            session_id,

            "role":
            user_role

        }

    }


    if tracer:

        config["callbacks"] = [
            tracer
        ]


    return config