import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from controllers.scheduler import Scheduler
from controllers.validator import TestScheduleCreate


@pytest.fixture
def scheduler():
    return Scheduler()


@pytest.fixture
def db_session():
    return MagicMock()


@patch('models.ciara_models.TestSchedule', autospec=True)
def test_mock_test_schedule_creation(mock_test_schedule, db_session):
    schedule_input = TestScheduleCreate(
        test_name="Test1",
        asset_name="Asset1",
        execution_time="2023-09-20T12:00:00",
        user_id=1
    )

    mock_test_schedule.return_value.id = 1

    scheduler = Scheduler()
    schedule_id = scheduler.add_schedule(schedule_input, db_session)
    assert schedule_id is None


def test_add_schedule_test_not_found(scheduler, db_session):
    schedule_input = TestScheduleCreate(
        test_name="NonExistentTest",
        asset_name="Asset1",
        execution_time="2023-09-20T12:00:00",
        user_id=1
    )

    db_session.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        scheduler.add_schedule(schedule_input, db_session)
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Test not found"


def test_add_schedule_internal_server_error(scheduler, db_session):
    schedule_input = TestScheduleCreate(
        test_name="Test1",
        asset_name="Asset1",
        execution_time="2023-09-20T12:00:00",
        user_id=1
    )

    db_session.add.side_effect = Exception("Database error")
    
    with pytest.raises(HTTPException) as exc_info:
        scheduler.add_schedule(schedule_input, db_session)
    
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Internal Server Error"
