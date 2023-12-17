import os
import sys


def getScriptDir():
    return getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

def getIconPath():
    script_dir = getScriptDir()
    icon_path = os.path.join(script_dir, "assets", "clock.ico")

    if os.path.exists(icon_path):
        return icon_path
    else:
        return None

    
def getDataPath():
    script_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(script_dir, "data", "preferences.json")

