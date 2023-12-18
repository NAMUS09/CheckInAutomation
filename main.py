import json
import os
from addToStartup import AddToStartup

from config_ui import ConfigUI
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

        self.cancelled = False

        data_path = getDataPath() 

        if not os.path.exists(data_path):
            self.cancelled = ConfigUI.showConfigUI()


        self.preference_exists = os.path.exists(data_path)

        if not self.cancelled and self.preference_exists:
            self.load_preferences()


    def load_preferences(self):
        data_path = getDataPath()

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
    if not AddToStartup.is_added_to_startup():
        AddToStartup.add_to_startup()

    app = CheckInApp()

    if not app.cancelled and app.preference_exists:
        app.check_in()
   