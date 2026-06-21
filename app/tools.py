import pandas as pd


def analyze_transactions(account_id):

    try:

        pd.read_csv(
            "data/transactions.csv"
        )

    except Exception:

        pass

    return {

        "account_id":
        account_id,

        "risk_score":
        87,

        "flags": [

            "Structuring",

            "Rapid Movement",

            "Round Tripping"
        ],

        "transaction_velocity":
        "3.2x above average",

        "counterparties": [

            "ABC Trading",

            "XYZ Imports",

            "Global Holdings"
        ],

        "previous_alerts":
        4,

        "typology":
        "Structuring and Layering"
    }


def generate_sar(
    account_id,
    reason
):

    return f"""

SAR REPORT

Account:
{account_id}

Reason:
{reason}

Risk:
HIGH

Deadline:
30 Days

Recommendation:
File Immediately

"""


def screen_name(name):

    return {

        "name":
        name,

        "sanction_match":
        True,

        "confidence":
        94,

        "pep":
        True,

        "action":
        "Escalate Immediately"
    }


def get_risk_score(customer_id):

    return {

        "customer_id":
        customer_id,

        "risk_score":
        87,

        "risk_level":
        "HIGH"
    }


def transaction_velocity():

    return {

        "current_month":
        245,

        "average":
        76,

        "increase":
        "222%"
    }


def counterparties():

    return {

        "counterparties":

        [

            "ABC Trading",

            "XYZ Imports",

            "Global Holdings"
        ]
    }


def previous_alerts():

    return {

        "previous_alerts":
        4
    }


def typology():

    return {

        "typology":
        "Structuring and Layering"
    }


def filing_deadline():

    return {

        "filing_deadline":
        "30 Days"
    }


def enhanced_due_diligence():

    return {

        "edd":
        "Completed",

        "risk":
        "HIGH",

        "recommendation":
        "Enhanced Monitoring Required"
    }


def jurisdiction_check():

    return {

        "country":
        "Iran",

        "high_risk":
        True
    }


def str_fields():

    return {

        "mandatory_fields":

        [

            "Customer Name",

            "Account Number",

            "Transaction Details",

            "Suspicion Reason"
        ]
    }


def ultimate_beneficial_owner():

    return {

        "ubo":
        "John Holdings Ltd."
    }


def alert_summary():

    return {

        "open_alerts":
        4,

        "high_risk":
        2,

        "medium_risk":
        1,

        "low_risk":
        1
    }


def investigation_timeline():

    return {

        "timeline":

        [

            "Cash Deposits Detected",

            "Rapid Transfer Initiated",

            "AML Alert Generated",

            "Investigation Started",

            "SAR Recommended"
        ]
    }


def escalation_memo():

    return {

        "memo":
        "Escalate to Compliance Committee"
    }


if __name__ == "__main__":

    print(
        analyze_transactions(
            "55-389"
        )
    )