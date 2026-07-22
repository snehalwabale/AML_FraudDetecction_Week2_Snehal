import os



def get_auth_headers(
    server_name:str
):

    """
    Generates authentication headers
    for MCP server communication
    """


    key_name = (

        server_name.upper()

        +

        "_API_KEY"

    )


    api_key = os.getenv(
        key_name
    )


    if not api_key:

        return {}



    return {


        "Authorization":

        f"Bearer {api_key}"

    }