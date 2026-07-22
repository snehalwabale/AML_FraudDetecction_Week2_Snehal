# hitl/store.py

from typing import Dict, List, Optional

from hitl.models import HITLTask


TASK_STORE: Dict[str, HITLTask] = {}



def create_task(task: HITLTask):
    """
    Save a HITL task
    """

    TASK_STORE[task.task_id] = task

    return task



def get_task(task_id: str) -> Optional[HITLTask]:
    """
    Fetch HITL task by ID
    """

    return TASK_STORE.get(task_id)



def get_pending_tasks() -> List[HITLTask]:
    """
    Return all pending HITL tasks
    """

    return [

        task

        for task in TASK_STORE.values()

        if task.status == "PENDING"

    ]



def update_task_status(
    task_id: str,
    status: str,
    comments: str = ""
):

    task = TASK_STORE.get(task_id)

    if not task:

        return {

            "status": "failed",

            "message": "Task not found"

        }

    task.status = status
    task.decision = status
    task.reviewer_comments = comments

    TASK_STORE[task_id] = task

    return task


def get_all_tasks():

    """
    Return all HITL tasks
    """

    return list(TASK_STORE.values())