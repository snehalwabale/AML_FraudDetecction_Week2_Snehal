import uuid

from datetime import datetime

from hitl.models import HITLTask

from hitl.store import TASK_STORE


def create_hitl_task(
    query,
    recommendation,
    reason="",
    role="Compliance Officer"
):

    task = HITLTask(

        task_id=str(uuid.uuid4()),

        trigger=reason if reason else "Critical AML Decision",

        query=query,

        recommendation=recommendation,

        role=role,

        status="Pending",

        created_at=datetime.utcnow()

    )

    TASK_STORE[task.task_id] = task

    return task.model_dump()

def list_pending_tasks():

    return [

        task

        for task in TASK_STORE.values()

        if task.status == "Pending"

    ]


def review_task(

    task_id,

    decision,

    comments

):

    if task_id not in TASK_STORE:

        return {

            "success": False,

            "message": "Task not found"

        }

    task = TASK_STORE[task_id]

    task.status = decision

    task.decision = decision

    task.reviewer_comments = comments

    return {

        "success": True,

        "task": task

    }