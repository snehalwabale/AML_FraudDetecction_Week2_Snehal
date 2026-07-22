from langchain_core.tools import StructuredTool

from mcp.client import (
    invoke_mcp_tool
)



def create_mcp_tool(
    server_name:str,
    description:str
):


    def execute(
        **kwargs
    ):

        return invoke_mcp_tool(

            server_name,

            kwargs

        )



    return StructuredTool.from_function(

        func=execute,

        name=server_name,

        description=description

    )




def load_mcp_tools():

    """
    Load MCP tools dynamically
    """

    from mcp.registry import list_servers


    tools=[]


    servers = list_servers()


    for server in servers:


        tool = create_mcp_tool(

            server["name"],

            server["description"]

        )


        tools.append(
            tool
        )


    return tools