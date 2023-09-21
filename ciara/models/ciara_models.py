from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base


from sqlalchemy.sql import func

class TestAsset(Base):
    __tablename__ = 'test_assets'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String)
    location = Column(String)
    availability = Column(String)


class Test(Base):
    __tablename__ = 'tests'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    executable_path = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TestSchedule(Base):
    __tablename__ = 'test_schedule'

    id = Column(Integer, primary_key=True)
    test_id = Column(Integer, ForeignKey('tests.id'))
    asset_id = Column(Integer, ForeignKey('test_assets.id'))
    execution_time = Column(DateTime(timezone=True))
    status = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    
    test = relationship("Test", backref="schedules")
    asset = relationship("TestAsset", backref="schedules")
    user = relationship("User", backref="schedules")


class TestExecutionResult(Base):
    __tablename__ = 'test_execution_result'

    id = Column(Integer, primary_key=True)
    schedule_id = Column(Integer, ForeignKey('test_schedule.id'))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    result = Column(String)
    log_file_path = Column(String)

    schedule = relationship("TestSchedule", backref="execution_results")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)