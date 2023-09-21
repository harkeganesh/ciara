import logging
import datetime
import subprocess
from models.ciara_models import Test
from models.database import SessionLocal
from models.ciara_models import TestSchedule, TestExecutionResult

logger = logging.getLogger(__name__)

class Executor:
    def execute_test(self, schedule_id: int):
        with SessionLocal() as db:
            test_schedule = db.query(TestSchedule).get(schedule_id)
            test = db.query(Test).filter(Test.id == test_schedule.test_id).first()
            
            if test_schedule and test:
                test_schedule.status = "running"
                db.commit()
                
                try:
                    # TODO Skipped execution result details intensionally for this exercise
                    # Also skipped the logic about asset on which this executable is running
                    # [test.executable_path]
                    executable = ["echo", "This is a test command. No actual testing performed."]

                    result = subprocess.run(executable,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE,
                                            text=True,
                                            check=True )
                    execution_result = TestExecutionResult(
                        schedule_id=test_schedule.id,
                        start_time=datetime.datetime.now(),
                        end_time=datetime.datetime.now(),
                        result=result.stdout if result.returncode == 0 else result.stderr,
                        log_file_path="path/to/logfile.txt"
                    )
                    db.add(execution_result)
                    
                    if result.returncode == 0:
                        test_schedule.status = "completed"
                    else:
                        test_schedule.status = "failed"
                    
                    db.commit()
                except Exception as e:
                    logger.error(f"Error executing test: {str(e)}")
                    test_schedule.status = "failed"
                    db.commit()
            
            else:
                logger.error(f"Schedule with ID {schedule_id} not found")

    
    