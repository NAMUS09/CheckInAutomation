import json
import os
import sys

from config import ConfigUI, preference_exists
from check_in import check_in_thread
from utils.common import getDataPath


class CheckInApp:
    def __init__(self):

        # Variables to store user preferences
        self.username =  ""
        self.password =  ""
        self.start_time =  ""
        self.end_time =  ""
        self.weekdays =  set()

        if not preference_exists():
            ConfigUI.showConfigUI()

        self.load_preferences()


    def load_preferences(self):
        if  preference_exists():
            script_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            data_path = os.path.join(script_dir, "data", "preferences.json") 
            with open(data_path, 'r') as file:
                preferences = json.load(file)
                self.username = preferences.get('username', '')
                self.password = preferences.get('password', '')
                self.start_time = preferences.get('start_time', '')
                self.end_time = preferences.get('end_time', '')
                self.weekdays = set(preferences.get('weekdays', []))
    
    def check_in(self):
        check_in_thread(self)


if __name__ == '__main__':
    app = CheckInApp()
    if preference_exists():
        app.check_in()
   