from fastapi import APIRouter, Header

from rbac.filter import (
    get_roles,
    get_role_permissions
)

from rbac.audit import (
    get_audit_logs
)


router = APIRouter(

    prefix="/rbac",

    tags=[
        "RBAC"
    ]

)


@router.get("/roles")
def roles():

    """
    List available RBAC roles.
    """

    return {

        "roles":
        get_roles()

    }


@router.get("/auth/context")
def auth_context(

    role: str = Header(
        default="analyst"
    )

):

    """
    Returns current user role
    and permissions.
    """

    permissions = get_role_permissions(

        role

    )

    return {

        "role":
        role,

        "permissions":
        permissions

    }


@router.get("/audit")
def audit_logs():

    """
    Returns RBAC audit logs.
    """

    return {

        "audit_logs":
        get_audit_logs()

    }