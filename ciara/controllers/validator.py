from datetime import datetime
from pydantic import BaseModel, PositiveInt


class TestScheduleCreate(BaseModel):
    test_name: str 
    asset_name: str
    execution_time: datetime
    user_id: PositiveInt


class TestScheduleResponse(BaseModel):
    id: int
    test_id: int
    asset_id: int
    execution_time: datetime
    status: str


class UserCreate(BaseModel):
    username: str
    password: str

