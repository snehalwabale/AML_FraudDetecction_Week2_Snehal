import requests

from mcp.registry import (
    get_server,
    get_available_tools
)

from mcp.auth import (
    get_auth_headers
)



def invoke_mcp_tool(
    server_name:str,
    payload:dict
):

    """
    Invoke MCP external tool
    """


    server = get_server(
        server_name
    )


    if not server:

        return {


            "status":
            "failed",


            "error":
            "MCP server not registered"

        }



    headers = get_auth_headers(
        server_name
    )


    try:


        response = requests.post(

            server["endpoint"],

            json=payload,

            headers=headers,

            timeout=3

        )


        return {


            "status":
            "success",


            "data":
            response.json()

        }



    except requests.exceptions.Timeout:


        return {


            "status":
            "failed",


            "error":
            "MCP server timeout"

        }



    except Exception as e:


        return {


            "status":
            "failed",


            "error":
            str(e)

        }




def discover_tools():

    """
    MCP tool discovery
    """

    return get_available_tools()