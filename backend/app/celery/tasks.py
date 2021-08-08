import time

from celery import Celery

from backend.config.settings import CELERY_BROKER_URL

celery = Celery("tasks", backend=CELERY_BROKER_URL, broker=CELERY_BROKER_URL)


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
