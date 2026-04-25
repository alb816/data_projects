import schedule
import time 
from main import main
from config import RUN_TIME

def run_scheduler():
    schedule.every().day.at(RUN_TIME).do(main)

    print("Scheduler started")
    while 1:
        schedule.run_pending()
        time.sleep(120)

if __name__ == "__main__":
    run_scheduler()