import os
import sys

def getIconPath():
    script_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    icon_path = os.path.join(script_dir, "assets", "clock.ico")

    if os.path.exists(icon_path):
        return icon_path
    else:
        return None


def getDataPath():
    data_directory = os.path.join(os.path.expanduser("~"), ".checkInAutomation")
    
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    return os.path.join(data_directory, "preferences.json")

