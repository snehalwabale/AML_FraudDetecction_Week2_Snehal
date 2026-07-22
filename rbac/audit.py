from datetime import datetime
import os
import json


AUDIT_FILE = "data/rbac_audit.json"


def log_rbac_event(

    user_role,

    query,

    documents

):
    """
    Log RBAC access events.
    """

    os.makedirs(
        "data",
        exist_ok=True
    )

    event = {

        "timestamp":
        datetime.utcnow().isoformat(),

        "role":
        user_role,

        "query":
        query,

        "documents_accessed":
        len(documents),

        "document_ids":[

            doc.metadata.get(
                "doc_id",
                "Unknown"
            )

            for doc in documents

        ]

    }

    logs = []

    if os.path.exists(AUDIT_FILE):

        try:

            with open(
                AUDIT_FILE,
                "r"
            ) as f:

                logs = json.load(f)

        except Exception:

            logs = []

    logs.append(event)

    with open(
        AUDIT_FILE,
        "w"
    ) as f:

        json.dump(
            logs,
            f,
            indent=4
        )

    return event


def get_audit_logs():

    if not os.path.exists(AUDIT_FILE):

        return []

    with open(
        AUDIT_FILE,
        "r"
    ) as f:

        return json.load(f)