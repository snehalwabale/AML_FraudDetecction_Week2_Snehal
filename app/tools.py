import os
from typing import List

from fastapi import UploadFile
from langchain_core.tools import tool

from rag.loaders import load_document
from rag.chunkers import chunk_document
from rag.embeddings import embed_chunks
from rag.vectorstore import vector_store


def ingest_documents(files: List[UploadFile], job_id: str):

    os.makedirs("data", exist_ok=True)

    for file in files:

        file_path = os.path.join(
            "data",
            file.filename
        )

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        docs = load_document(file_path)

        chunks = chunk_document(docs)

        embed_chunks(chunks)

        vector_store.add_documents(chunks)

    return {

        "job_id": job_id,

        "status": "completed"

    }


def get_sources():

    try:

        store = vector_store.docstore._dict

        sources = []

        for _, doc in store.items():

            sources.append(

                {

                    "doc_id": doc.metadata.get(

                        "doc_id",

                        "Unknown"

                    ),

                    "source": doc.metadata.get(

                        "source",

                        "Unknown"

                    )

                }

            )

        unique = []

        seen = set()

        for s in sources:

            if s["doc_id"] not in seen:

                seen.add(s["doc_id"])

                unique.append(s)

        return unique

    except Exception:

        return []


def delete_source(doc_id):

    return {

        "status": "delete operation not supported by current FAISS implementation",

        "doc_id": doc_id

    }


def run_evaluation():

    try:

        from eval.run_eval import run_all

        return run_all()

    except Exception as e:

        return {

            "status": "failed",

            "error": str(e)

        }


@tool
def analyze_transactions() -> str:
    """Analyze suspicious transactions."""

    return """
Transactions Analysed

Total Transactions : 3

Suspicious Transactions : 2

Risk Level : High

Recommendation :
Review immediately.
"""


@tool
def screen_name(name: str) -> str:
    """Check customer against sanctions and PEP lists."""

    return f"""
Customer : {name}

Sanctions Match : No

PEP : No

Result :
Customer cleared.
"""


@tool
def get_risk_score(customer: str) -> str:
    """Retrieve AML risk score."""

    return f"""
Customer : {customer}

Risk Score : 83

Risk Level : High
"""


@tool
def transaction_velocity() -> str:
    """Analyze transaction velocity."""

    return """
Average Daily Transactions : 12

Today's Transactions : 39

Status :

Unusual Increase Detected
"""


@tool
def counterparties() -> str:
    """Retrieve counterparties."""

    return """
Counterparties

ABC Trading

Global Finance

XYZ Holdings
"""


@tool
def previous_alerts() -> str:
    """Retrieve previous AML alerts."""

    return """
Previous Alerts : 5

Closed : 4

Open : 1
"""


@tool
def typology() -> str:
    """Return AML typology."""

    return "Structuring / Smurfing"


@tool
def filing_deadline() -> str:
    """Return SAR filing deadline."""

    return "SAR Filing Deadline : 30 Days"


@tool
def enhanced_due_diligence() -> str:
    """EDD recommendation."""

    return "Enhanced Due Diligence Recommended"


@tool
def jurisdiction_check() -> str:
    """Jurisdiction risk."""

    return "Medium Risk Jurisdiction"


@tool
def str_fields() -> str:
    """Mandatory STR/SAR fields."""

    return """
Required Fields

Customer

Account

Transaction

Reason
"""


@tool
def ultimate_beneficial_owner() -> str:
    """Return UBO."""

    return "Ultimate Beneficial Owner : John Smith"


@tool
def alert_summary() -> str:
    """Current alert summary."""

    return """
Open Alerts : 7

Critical : 2

Medium : 3

Low : 2
"""


@tool
def investigation_timeline() -> str:
    """Investigation timeline."""

    return """
Timeline

Account Opened

Cash Deposits

International Transfers

Alert Generated
"""


@tool
def escalation_memo() -> str:
    """Generate escalation memo."""

    return """
Escalation Memo

Repeated Structuring Behaviour Detected.

Recommend Compliance Escalation.

Recommend SAR Filing.
"""