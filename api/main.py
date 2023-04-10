import time
import uvicorn
import schedule

from fastapi import FastAPI
from main_tracking import endpoint


app = FastAPI()

if __name__ == "__main__":

    app.include_router(endpoint.router)


    uvicorn.run(app, host="0.0.0.0", port=4545)
    while True:
        schedule.run_pending()
        time.sleep(1)