
import os
import shutil
import winreg as reg

from tkinter import messagebox


def show_message(message):
    messagebox.showinfo("CheckInAutomation", message)

def deleteDirectory():
    data_directory = os.path.join(os.path.expanduser("~"), ".checkInAutomation")
    
    if os.path.exists(data_directory):
        shutil.rmtree(data_directory)

import winreg as reg

def remove_from_startup():
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    entry_name = "CheckInAutomation"

    try:
        # Open the registry key for editing
        with reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_SET_VALUE) as registry_key:
            # Delete the specified entry from the registry key
            reg.DeleteValue(registry_key, entry_name)
        print(f"Entry '{entry_name}' removed from startup successfully.")

        # delete app directory
        deleteDirectory()

        # display message
        show_message("CheckInAutomation uninstalled successfully")
        
    except FileNotFoundError:
        print("Registry key not found or entry does not exist in startup.")

         # display message
        show_message("CheckInAutomation not installed")


if __name__ == '__main__':
    # remove from the startup
    remove_from_startup()
   