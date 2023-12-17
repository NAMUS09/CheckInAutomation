import os
import sys


def getIconPath():
    script_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    icon_path = os.path.join(script_dir, "assets", "clock.ico")

    if os.path.exists(icon_path):
        return icon_path
    else:
        return None
