import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.ciara_models import Test, TestAsset, TestSchedule
from controllers.validator import TestScheduleCreate


class Scheduler:
    def add_schedule(self, schedule: TestScheduleCreate, db: Session,
                     status: str = "pending") -> int:
        try:
            test = db.query(Test).filter(Test.name == schedule.test_name).first()
            asset = db.query(TestAsset).filter(TestAsset.name == 
                                                schedule.asset_name).first()
            if self._validate_schedule(test, asset):
                db_schedule = TestSchedule(
                    test_id=test.id,
                    asset_id=asset.id,
                    execution_time=schedule.execution_time,
                    user_id=schedule.user_id,
                    status=status,
                )
                db.add(db_schedule)
                db.commit()
                db.flush()
                schedule_id = db_schedule.id
                db.close()

                return schedule_id
        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error while adding the record {e}")
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            db.close()

    def _validate_schedule(self, test: Test, asset: TestAsset) -> bool:
        if not test:
            raise HTTPException(status_code=400, detail="Test not found")
        if not asset:
            raise HTTPException(status_code=400, detail="Asset not found")
        return True