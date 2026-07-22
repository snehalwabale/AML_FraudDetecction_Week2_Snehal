from fastapi import APIRouter

from pydantic import BaseModel

from mcp.client import (
    discover_tools,
    invoke_mcp_tool
)


router = APIRouter(
    prefix="/mcp",
    tags=["MCP"]
)



class MCPInvokeRequest(BaseModel):

    tool_name: str

    parameters: dict = {}



@router.get("/tools")
def list_mcp_tools():

    """
    List all registered MCP tools
    """

    return {

        "tools":
        discover_tools()

    }



@router.post("/invoke")
def invoke_tool(
    request: MCPInvokeRequest
):

    """
    Invoke MCP tool dynamically
    """


    return invoke_mcp_tool(

        request.tool_name,

        request.parameters

    )