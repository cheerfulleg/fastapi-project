import time

from celery import Celery


celery = Celery("tasks", backend="redis://127.0.0.1:6379/0", broker="redis://127.0.0.1:6379/0")

# celery.conf.broker_url = 'redis://127.0.0.1:6379/0'
# celery.conf.result_backend = 'redis://'


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True
