import os
import sys
import winreg as reg


class AddToStartup:

    def __init__(self):
        self.app_name = "CheckInAutomation"


    def is_added_to_startup(self):
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_READ) as registry_key:
                value, _ = reg.QueryValueEx(registry_key, self.app_name)
                return value.lower() == f'"{sys.executable}" "{os.path.abspath(__file__)}"'.lower()
        except FileNotFoundError:
            return False

    def add_to_startup(self):
        if not self.is_added_to_startup():
            python_path = sys.executable
            script_path = os.path.abspath(__file__)

            with reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE) as registry_key:
                reg.SetValueEx(registry_key,  self.app_name, 0, reg.REG_SZ, f'"{python_path}" "{script_path}"')

