import json

from tkinter import messagebox
from datetime import datetime 
from config import  preference_exists, load_config_ui
from check_in import check_in, should_check_in



def show_message(message):
    messagebox.showinfo("Check-In Status", message)

class CheckInApp:
    def __init__(self):

        # Variables to store user preferences
        self.username =  ""
        self.password =  ""
        self.start_time =  ""
        self.end_time =  ""
        self.weekdays =  set()

        if not preference_exists():
            load_config_ui()

        self.load_preferences()

        print(f"Username: {self.username}")
        print(f"Password: {self.password}")
        print(f"Start Time: {self.start_time}")
        print(f"End Time: {self.end_time}")
        print(f"Weekdays: {list(self.weekdays)}")


    def load_preferences(self):
        if  preference_exists():
            with open('preferences.json', 'r') as file:
                preferences = json.load(file)
                self.username = preferences.get('username', '')
                self.password = preferences.get('password', '')
                self.start_time = preferences.get('start_time', '')
                self.end_time = preferences.get('end_time', '')
                self.weekdays = set(preferences.get('weekdays', []))


    def check_in_thread(self):
        current_day = datetime.now().weekday()

        if should_check_in(self):
            status = check_in(self)
            show_message(status)
        elif current_day not in self.weekdays:
            show_message("Check-in not triggered - Today is not a configured weekday")
        else:
            show_message("Check-in not triggered - Not within the configured time frame")



if __name__ == '__main__':
    app = CheckInApp()
    if preference_exists():
        print("preference exits")
        app.check_in_thread()
   