import os
import yaml


CONFIG_PATH = "config/mcp_servers.yaml"



def load_mcp_servers():

    if not os.path.exists(CONFIG_PATH):

        return []


    with open(
        CONFIG_PATH,
        "r"
    ) as file:

        config = yaml.safe_load(file)


    return config.get(
        "servers",
        []
    )



def list_servers():

    """
    Returns all registered MCP servers
    """

    return load_mcp_servers()



def get_server(
    server_name: str
):

    """
    Get MCP server configuration
    """

    servers = load_mcp_servers()


    for server in servers:

        if server["name"] == server_name:

            return server


    return None



def get_available_tools():

    """
    MCP discovery endpoint response
    """

    tools = []


    for server in load_mcp_servers():

        tools.append(

            {

                "name":
                server["name"],


                "description":
                server["description"],


                "endpoint":
                server["endpoint"]

            }

        )


    return tools