import os
import sys
import winreg as reg

def is_added_to_startup():
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_READ) as registry_key:
            value, _ = reg.QueryValueEx(registry_key, "MyPythonApp")
            return value.lower() == f'"{sys.executable}" "{os.path.abspath(__file__)}"'.lower()
    except FileNotFoundError:
        return False

def add_to_startup():
    if not is_added_to_startup():
        python_path = sys.executable
        script_path = os.path.abspath(__file__)

        with reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE) as registry_key:
            reg.SetValueEx(registry_key, "MyPythonApp", 0, reg.REG_SZ, f'"{python_path}" "{script_path}"')
