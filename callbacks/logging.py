import logging
import json
from datetime import datetime


logger = logging.getLogger(
    "aml_fraud_copilot"
)


logger.setLevel(
    logging.INFO
)


handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(message)s"
)

handler.setFormatter(
    formatter
)


logger.addHandler(
    handler
)



def log_event(
    event_type: str,
    data: dict
):

    payload = {

        "timestamp":
        datetime.utcnow().isoformat(),

        "event":
        event_type,

        "data":
        data

    }


    logger.info(
        json.dumps(
            payload
        )
    )


def log_chain_start(
    chain_name,
    input_data
):

    log_event(

        "CHAIN_START",

        {

            "chain":
            chain_name,

            "input":
            input_data

        }

    )


def log_chain_end(
    chain_name,
    output
):

    log_event(

        "CHAIN_END",

        {

            "chain":
            chain_name,

            "output":
            output

        }

    )


def log_tool_execution(
    tool_name,
    result
):

    log_event(

        "TOOL_EXECUTION",

        {

            "tool":
            tool_name,

            "result":
            result

        }

    )