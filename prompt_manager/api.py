# prompt_manager/api.py

from fastapi import APIRouter

from prompt_manager.registry import (
    list_prompts,
    get_prompt_history,
    activate_prompt_version
)

from pydantic import BaseModel


router = APIRouter(

    prefix="/prompts",

    tags=["Prompt Management"]

)



class ActivatePromptRequest(BaseModel):

    version: str



@router.get("")
def prompts():

    """
    List all prompt templates
    with active versions
    """

    return {

        "prompts": list_prompts()

    }



@router.get("/{name}/history")
def prompt_history(

    name: str

):

    """
    Get prompt version history
    """

    return {

        "name": name,

        "history": get_prompt_history(name)

    }



@router.post("/{name}/activate")
def activate_version(

    name: str,

    request: ActivatePromptRequest

):

    """
    Rollback or activate
    specific prompt version
    """

    result = activate_prompt_version(

        name,

        request.version

    )


    return {

        "prompt": name,

        "active_version": request.version,

        "result": result

    }