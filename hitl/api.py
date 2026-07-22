# hitl/api.py

from fastapi import APIRouter

from hitl.store import (
    get_pending_tasks,
    update_task_status,
    get_task
)

from pydantic import BaseModel



router = APIRouter(

    prefix="/hitl",

    tags=["HITL"]

)



class HITLReviewRequest(BaseModel):

    decision: str

    comments: str = ""



@router.get("/pending")
def pending_tasks():

    return {

        "pending_tasks":
        get_pending_tasks()

    }



@router.post("/review/{task_id}")
def review_task(

    task_id: str,

    request: HITLReviewRequest

):

    decision = request.decision.lower()



    if decision not in [

        "approve",

        "reject"

    ]:

        return {

            "status": "failed",

            "message":
            "Decision must be approve or reject"

        }



    result = update_task_status(

        task_id,

        decision.upper(),

        request.comments

    )



    return {

        "task_id":

        task_id,


        "decision":

        decision,


        "comments":

        request.comments,


        "result":

        result

    }



@router.get("/task/{task_id}")
def task_details(

    task_id: str

):

    return get_task(task_id)