import json
import os

from datetime import datetime

LOG_FOLDER = "logs"

LOG_FILE = os.path.join(

    LOG_FOLDER,

    "interactions.json"

)

os.makedirs(

    LOG_FOLDER,

    exist_ok=True

)


def log_interaction(

    session_id,

    query,

    response,

    tool_used,

    level="INFO"

):

    log = {

        "timestamp": datetime.now().isoformat(),

        "level": level,

        "session_id": session_id,

        "query": query,

        "response": response,

        "tool_used": tool_used

    }

    with open(

        LOG_FILE,

        "a",

        encoding="utf-8"

    ) as f:

        f.write(

            json.dumps(

                log,

                ensure_ascii=False

            )

            + "\n"

        )


def log_error(

    session_id,

    error,

    query=""

):

    log = {

        "timestamp": datetime.now().isoformat(),

        "level": "ERROR",

        "session_id": session_id,

        "query": query,

        "error": str(error)

    }

    with open(

        LOG_FILE,

        "a",

        encoding="utf-8"

    ) as f:

        f.write(

            json.dumps(

                log,

                ensure_ascii=False

            )

            + "\n"

        )


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

    ) as f:

        for line in f:

            line = line.strip()

            if not line:

                continue

            try:

                logs.append(

                    json.loads(line)

                )

            except Exception:

                pass

    return logs


def get_session_logs(

    session_id

):

    logs = read_logs()

    return [

        log

        for log in logs

        if log.get(

            "session_id"

        ) == session_id

    ]


def clear_logs():

    if os.path.exists(

        LOG_FILE

    ):

        open(

            LOG_FILE,

            "w"

        ).close()


def log_count():

    return len(

        read_logs()

    )