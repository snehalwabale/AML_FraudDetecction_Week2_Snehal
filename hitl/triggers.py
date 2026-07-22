HITL_KEYWORDS = [

    "sar",
    "str",
    "freeze account",
    "freeze transaction",
    "sanction match",
    "pep onboarding",
    "file report",
    "suspicious activity",
    "manual review"

]


def should_trigger_hitl(query: str):

    """
    Determine whether Human-In-The-Loop approval is required.

    Returns:
        tuple:
            (True/False, reason)
    """

    if not query:
        return False, ""

    query = query.lower()


    for keyword in HITL_KEYWORDS:

        if keyword in query:

            return (
                True,
                f"HITL triggered because request contains restricted keyword: '{keyword}'"
            )


    return False, ""