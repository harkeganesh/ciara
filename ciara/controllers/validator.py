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


class TestBase(BaseModel):
    name: str
    executable_path: str

class TestCreate(TestBase):
    pass

class TestUpdate(TestBase):
    pass

class TestSchema(TestBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TestAssetBase(BaseModel):
    name: str
    type: str
    status: str
    location: str
    availability: str

class TestAssetCreate(TestAssetBase):
    pass

class TestAssetUpdate(TestAssetBase):
    pass

class TestAssetSchema(TestAssetBase):
    id: int

    class Config:
        orm_mode = True
