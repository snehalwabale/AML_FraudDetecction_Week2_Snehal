import yaml
import os


ROLE_CONFIG = "config/roles.yaml"


def load_roles():

    if not os.path.exists(ROLE_CONFIG):

        return {}

    with open(
        ROLE_CONFIG,
        "r"
    ) as file:

        data = yaml.safe_load(file) or {}

    return data.get(
        "roles",
        {}
    )


def get_roles():

    return load_roles()


def get_role_permissions(role):

    roles = load_roles()

    return roles.get(
        role,
        {}
    )


def get_allowed_doc_types(role):

    permissions = get_role_permissions(
        role
    )

    return permissions.get(
        "allowed_doc_types",
        []
    )


def apply_role_filter(
    documents,
    role
):

    """
    Apply RBAC filtering before sending retrieved
    documents to the LLM.
    """

    allowed = get_allowed_doc_types(
        role
    )

    # No restrictions configured -> allow everything
    if not allowed:

        return documents

    filtered = []

    for doc in documents:

        doc_type = doc.metadata.get(
            "doc_type",
            "general"
        )

        if doc_type in allowed:

            filtered.append(doc)

    return filtered