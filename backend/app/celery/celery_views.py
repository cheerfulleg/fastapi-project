from celery.result import AsyncResult
from fastapi import APIRouter
from starlette.responses import JSONResponse

from .schemas import CeleryBody, TaskStatus
from .tasks import create_task, celery

celery_router = APIRouter()


@celery_router.post("/tasks", status_code=201)
def run_task(payload: CeleryBody):
    """
    Sends int value, delays for this value * 10 sec
    """
    task_type = payload.dict()["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@celery_router.get("/tasks/{task_id}", response_model=TaskStatus)
def get_status(task_id: str):
    """
    Returns status of celery task by task id, got from /tasks endpoint
    """
    task_result = AsyncResult(task_id, app=celery)
    # result = {"task_id": task_id, "task_status": task_result.status, "task_result": task_result.result}
    result = TaskStatus(task_id=task_id, task_status=task_result.status, task_result=task_result.result)
    return result
