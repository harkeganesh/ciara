import logging
import os

from celery import Celery

from controllers.executor import Executor

logger = logging.getLogger(__name__)

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", 
                                            "redis://localhost:6379")


@celery.task
def execute_test(schedule_id: int):
    executor = Executor()
    executor.execute_test(schedule_id)
    return True
