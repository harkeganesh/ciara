import logging
from typing import Annotated
import pytz

from celery.result import AsyncResult
from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.orm import Session
from models.session import get_db

from worker import execute_test

from controllers.validator import TestScheduleCreate
from controllers.scheduler import Scheduler


logger = logging.getLogger(__name__)


db_session = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/orchestrator",
                   tags=["Test Orchestrator"],
                   responses={404: {"description": "Not found."}})



@router.post("/schedule", status_code=status.HTTP_201_CREATED)
async def create_test_schedule(schedule: TestScheduleCreate, 
                               db: db_session):
    test_scheduler = Scheduler()
    
    test_schedule_id = test_scheduler.add_schedule(schedule, db, status="pending")   

    if test_schedule_id:
        execution_time = schedule.execution_time.astimezone(pytz.UTC)
        schedule = execute_test.apply_async(args=(test_schedule_id,), eta=execution_time)
        logger.info(f"Test is scheduled with Schedule ID: {schedule.id} and will run at\
                    {execution_time} UTC")
        return {"message": schedule.id}
    return {"message": "Test details not found."}


@router.get("/schedule/{schedule_id}")
def get_status(schedule_id):
    schedule_result = AsyncResult(schedule_id)
    result = {
        "task_id": schedule_id,
        "task_status": schedule_result.status,
        "task_result": schedule_result.result
    }
    return result