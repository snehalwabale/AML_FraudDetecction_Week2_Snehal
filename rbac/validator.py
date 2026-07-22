from rbac.filter import (
    get_allowed_doc_types
)


def validate_documents(
    documents,
    role
):
    """
    Perform post-retrieval RBAC validation.
    Ensures only authorized documents are returned.
    """

    allowed = get_allowed_doc_types(
        role
    )

    # If no restrictions are configured,
    # allow all retrieved documents.
    if not allowed:

        return documents

    validated = []

    for doc in documents:

        doc_type = doc.metadata.get(
            "doc_type",
            "general"
        )

        if doc_type in allowed:

            validated.append(doc)

    return validated