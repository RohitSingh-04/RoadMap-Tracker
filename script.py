import pandas as pd
import json
import os
import plyer 
from datetime import date, timedelta, datetime
from time import sleep 

class Tracker:
    ALL_Tasks = pd.read_csv("roadmap.csv")
    USER_PROGRESS = {}
    USER_FILE_POINTER = None 
    APP_NAME = "RoadMap Tracker"
    TIMEOUT = 100
    APP_ICON = "icon/favicon.ico"

    def __init__(self, app_name = None, app_icon = None):

        if app_name:
            self.APP_NAME = app_name
        if app_icon:
            self.APP_ICON = app_icon
        
        if not os.path.exists("progress.json"):
            self.USER_PROGRESS = {"dates": [{str(date.today()+ timedelta(day)):[]} for day in range(len(self.ALL_Tasks))]} | {"streak": 0 , "start_date": str(date.today())}
            self.USER_FILE_POINTER = open("progress.json", "w")
            json.dump(self.USER_PROGRESS, self.USER_FILE_POINTER)
        else:
            self.USER_FILE_POINTER = open("progress.json", "r")
            self.USER_PROGRESS = json.load(self.USER_FILE_POINTER)

        self.USER_FILE_POINTER.close()
    
    def check_today(self) -> bool:
        number_of_tasks_today  = len(self.USER_PROGRESS["dates"][int((date.today() - datetime.strptime(self.USER_PROGRESS["start_date"], "%Y-%m-%d").date()).days)][str(date.today())])

        if number_of_tasks_today == 0:
            self.send_notification(0)
            return False
        else:
            self.send_notification(number_of_tasks_today)
            return True
    
    def send_notification(self, number_of_tasks):
        if number_of_tasks == 0:
            plyer.notification.notify(app_name = self.APP_NAME, title = "Tasks Pending!", message = f"you do not have completed your taks! 0 tasks completed 😟!", timeout = self.TIMEOUT, app_icon = self.APP_ICON)
        else:
            plyer.notification.notify(app_name = self.APP_NAME, title="Congrats!", message = f"you have completed {number_of_tasks} Tasks today 😍", timeout = self.TIMEOUT, app_icon = self.APP_ICON)

while True:
    t = Tracker()
    if t.check_today():
        break
    del t
    sleep(10800)