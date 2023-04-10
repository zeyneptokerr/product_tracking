import time
import schedule

from fastapi import FastAPI
from .database import db_operations

app = FastAPI()

class VacuumCleaner:
    if __name__ == "__main__":

        schedule.every(1).hours.do(db_operations.get_tracked_products)

        while True:
            schedule.run_pending()
            time.sleep(1)