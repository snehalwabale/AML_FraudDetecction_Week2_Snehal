import os
from typing import List

from fastapi import UploadFile

from rag.loaders import load_document
from rag.chunkers import chunk_document
from rag.embeddings import embed_chunks
from rag.vectorstore import vector_store


def ingest_documents(files: List[UploadFile], job_id: str):

    os.makedirs("data", exist_ok=True)

    for file in files:

        file_path = os.path.join("data", file.filename)

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
                    "doc_id": doc.metadata.get("doc_id", "Unknown"),
                    "source": doc.metadata.get("source", "Unknown")
                }
            )

        unique = []
        seen = set()

        for item in sources:

            if item["doc_id"] not in seen:
                seen.add(item["doc_id"])
                unique.append(item)

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


def analyze_transactions():

    return """
Transactions Analysed

Total Transactions : 3

Suspicious Transactions : 2

Risk Level : High

Recommendation :
Review immediately.
"""


def screen_name(name="Unknown"):

    return f"""
Customer : {name}

Sanctions Match : No

PEP : No

Result :
Customer cleared.
"""


def get_risk_score(customer="Unknown"):

    return f"""
Customer : {customer}

Risk Score : 83

Risk Level : High
"""


def transaction_velocity():

    return """
Average Daily Transactions : 12

Today's Transactions : 39

Status :

Unusual Increase Detected
"""


def counterparties():

    return """
Counterparties

ABC Trading

Global Finance

XYZ Holdings
"""


def previous_alerts():

    return """
Previous Alerts : 5

Closed : 4

Open : 1
"""


def typology():

    return "Structuring / Smurfing"


def filing_deadline():

    return "SAR Filing Deadline : 30 Days"


def enhanced_due_diligence():

    return "Enhanced Due Diligence Recommended"


def jurisdiction_check():

    return "Medium Risk Jurisdiction"


def str_fields():

    return """
Required Fields

Customer

Account

Transaction

Reason
"""


def ultimate_beneficial_owner():

    return "Ultimate Beneficial Owner : John Smith"


def alert_summary():

    return """
Open Alerts : 7

Critical : 2

Medium : 3

Low : 2
"""


def investigation_timeline():

    return """
Timeline

Account Opened

Cash Deposits

International Transfers

Alert Generated
"""


def escalation_memo():

    return """
Escalation Memo

Repeated Structuring Behaviour Detected.

Recommend Compliance Escalation.

Recommend SAR Filing.
"""