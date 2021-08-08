from celery.result import AsyncResult
from fastapi import APIRouter, Body
from starlette.responses import JSONResponse

from .tasks import create_task, celery

celery_router = APIRouter()


@celery_router.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@celery_router.get("/tasks/{task_id}")
def get_status(task_id):
    task_result = AsyncResult(task_id, app=celery)
    result = {"task_id": task_id, "task_status": task_result.status, "task_result": task_result.result}
    return JSONResponse(result)
