import datetime

from tkinter import messagebox
from check_in import check_in, should_check_in


def show_message(message):
    messagebox.showinfo("Check-In Status", message)


class CheckInApp:
    @staticmethod
    def check_in_thread():
        if should_check_in():
            status = check_in()
            show_message(status)
        else:
            day = datetime.datetime.now().weekday()
            if day == 5 or day == 6:
                show_message("Check-in not triggered - Weekdays")
            else:
                show_message("Check-in not triggered - Not within the time frame (9 - 11)")

    check_in_thread()


if __name__ == '__main__':
    CheckInApp()
