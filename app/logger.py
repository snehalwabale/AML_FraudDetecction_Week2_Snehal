import json
import os

from datetime import datetime


# =====================================================
# LOG FILE LOCATION
# =====================================================

LOG_FOLDER = "logs"

LOG_FILE = "logs/interactions.json"


# =====================================================
# CREATE LOG DIRECTORY
# =====================================================

os.makedirs(
    LOG_FOLDER,
    exist_ok=True
)


# =====================================================
# LOG INTERACTION
# =====================================================

def log_interaction(

    session_id,

    query,

    response,

    tool_used

):

    log_entry = {

        "timestamp":
        str(datetime.now()),

        "session_id":
        session_id,

        "query":
        query,

        "response":
        response,

        "tool_used":
        tool_used
    }

    with open(

        LOG_FILE,

        "a",

        encoding="utf-8"

    ) as file:

        file.write(

            json.dumps(
                log_entry
            )

            + "\n"
        )


# =====================================================
# READ LOGS
# =====================================================

def read_logs():

    if not os.path.exists(
        LOG_FILE
    ):

        return []

    logs = []

    with open(

        LOG_FILE,

        "r",

        encoding="utf-8"

    ) as file:

        for line in file:

            try:

                logs.append(
                    json.loads(
                        line
                    )
                )

            except:

                pass

    return logs