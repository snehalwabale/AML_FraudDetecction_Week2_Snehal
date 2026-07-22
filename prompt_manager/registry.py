# prompt_manager/registry.py

import os
import json


REGISTRY_FILE = "data/prompt_registry.json"



def ensure_registry():

    directory = os.path.dirname(REGISTRY_FILE)


    if not os.path.exists(directory):

        os.makedirs(directory)



    if not os.path.exists(REGISTRY_FILE):

        with open(REGISTRY_FILE, "w") as file:

            json.dump({}, file)




def load_registry():

    ensure_registry()

    with open(REGISTRY_FILE, "r") as file:

        return json.load(file)




def save_registry(data):

    ensure_registry()

    with open(REGISTRY_FILE, "w") as file:

        json.dump(

            data,

            file,

            indent=4

        )




def register_prompt(

    name: str,

    version: str

):

    registry = load_registry()


    if name not in registry:

        registry[name] = {

            "versions": [],

            "active_version": version

        }



    if version not in registry[name]["versions"]:

        registry[name]["versions"].append(version)



    registry[name]["active_version"] = version


    save_registry(registry)


    return registry[name]




def list_prompts():

    """
    List all registered prompts
    with active versions.
    """

    registry = load_registry()


    result = []


    for name, data in registry.items():

        result.append(

            {

                "name": name,

                "active_version": data.get(
                    "active_version"
                ),

                "versions": data.get(
                    "versions",
                    []
                )

            }

        )


    return result




def get_prompt_history(

    name: str

):

    registry = load_registry()


    return registry.get(

        name,

        {

            "versions": [],

            "active_version": None

        }

    )




def activate_prompt_version(

    name: str,

    version: str

):

    registry = load_registry()



    if name not in registry:

        return {

            "status": "failed",

            "message": "Prompt not found"

        }




    if version not in registry[name]["versions"]:

        return {

            "status": "failed",

            "message": "Version not available"

        }




    registry[name]["active_version"] = version



    save_registry(registry)



    return {

        "status": "success",

        "prompt": name,

        "active_version": version

    }