import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.ciara_models import Test
from controllers.validator import  TestCreate
from models.session import get_db


logger = logging.getLogger(__name__)


db_session = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/tests",
                   tags=["Test Manager"],
                   responses={404: {"description": "Not found."}})


# for demo purpose only not recommended for production
@router.get("/all_tests")
def get_all_tests(db: db_session):
    tests = db.query(Test).all()
    return tests


@router.get("/{test_id}")
def read_test(test_id: int, db: db_session):
    db_test = db.query(Test).filter(Test.id == test_id).first()
    if db_test is None:
        raise HTTPException(status_code=404, detail="Test not found")
    return db_test


@router.post("/")
def create_test(test: TestCreate, db: db_session):
    db_test = Test(**test.dict())
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

