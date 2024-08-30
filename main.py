import os
from UI.config_ui import ConfigUI
from core.check_in import check_in_thread
from utils import add_to_startup, is_added_to_startup, decrypt_data, getDataPath,get_old_exe_paths,get_current_app_version,show_message
from utils.os import delete_file


class CheckInApp:
    def __init__(self):

        # Variables to store user preferences
        self.username =  ""
        self.password =  ""
        # self.status_type = ""
        # self.session_type = ""
        self.start_time =  ""
        self.end_time =  ""
        self.weekdays =  set()
        self.appVersion = ""

        self.cancelled = False

        data_path = getDataPath() 

        if not os.path.exists(data_path):
            self.cancelled = ConfigUI.showConfigUI().get("cancelled")


        self.preference_exists = os.path.exists(data_path)

        if not self.cancelled and self.preference_exists:
            self.load_preferences()

    
    def load_preferences(self):
        data_path = getDataPath()

        with open(data_path, 'rb') as file:
            encrypted_data = file.read()
            preferences = decrypt_data(encrypted_data)

        self.username = preferences.get('username', '')
        self.password = preferences.get('password', '')
        # self.status_type = preferences.get('status_type', '')
        # self.session_type = preferences.get('status_session', '')
        self.start_time = preferences.get('start_time', '')
        self.end_time = preferences.get('end_time', '')
        self.weekdays = set(preferences.get('weekdays', []))

    def validate_saved_data(self):
        if not self.username:
            return False
        if not self.password:
            return False
        # if not self.status_type:
        #     return False 
        # if not self.session_type:
        #     return False
        if not self.start_time:
            return False 
        if not self.end_time:
            return False 
        if not self.weekdays:
            return False 
        return True
    
    def check_in(self):
        validate = self.validate_saved_data()
        if not validate:
            response = ConfigUI.showConfigUI(edit=True)
            if response.get("cancelled"):
                show_message("Error","Check-in cancelled. Please update all configurations before checking in the timesheet.")
                return
            
            if response.get("saved"):
                # load again updated data
                self.load_preferences()

        check_in_thread(self)


if __name__ == '__main__':
    if not is_added_to_startup():
        add_to_startup()

    # Get old exe paths, if exists in current app executable directory
    old_exe_paths = get_old_exe_paths(get_current_app_version())

    if old_exe_paths and len(old_exe_paths) > 0:
        for path in old_exe_paths:
            # Delete the old executable files
            delete_file(path)

    app = CheckInApp()

    if not app.cancelled and app.preference_exists:
        app.check_in()
   