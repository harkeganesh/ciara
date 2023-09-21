from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


@pytest.fixture
def mock_scheduler():
    with patch('router.orchestrator.Scheduler') as mock_scheduler:
        yield mock_scheduler


@pytest.fixture
def mock_execute_test():
    with patch('router.orchestrator.execute_test.apply_async') as mock_task:
        yield mock_task


def test_create_test_schedule(mock_scheduler, mock_execute_test):
    mock_schedule_instance = mock_scheduler.return_value
    mock_schedule_instance.add_schedule.return_value = 1

    mock_task_instance = mock_execute_test.return_value
    mock_task_instance.id = 'dummy_task_id'

    schedule_input = {
        "test_name": "Test1",
        "asset_name": "Asset1",
        "execution_time": "2023-09-20T12:00:00",
        "user_id": 1
    }

    response = client.post("/orchestrator/schedule", json=schedule_input)

    assert response.status_code == 201

    assert response.json() == {"message": 'dummy_task_id'}


def test_create_test_schedule_test_schedule_id_not_returned(mock_scheduler):
    mock_schedule_instance = mock_scheduler.return_value
    mock_schedule_instance.add_schedule.return_value = None

    schedule_input = {
        "test_name": "Test1",
        "asset_name": "Asset1",
        "execution_time": "2023-09-20T12:00:00",
        "user_id": 1
    }
    response = client.post("/orchestrator/schedule", json=schedule_input)

    assert response.status_code == 201

    assert response.json() == {"message": "Test details not found."}
