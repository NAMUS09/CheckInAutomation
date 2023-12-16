import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font
from timePicker import TimePicker


def show_message(message):
    messagebox.showinfo("Configuration Alert", message)


def preference_exists():
    return os.path.exists('preferences.json')

     
class ConfigUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuration")

        # Variables to store user input
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.start_time_var = tk.StringVar(value="09:00")
        self.end_time_var = tk.StringVar(value="11:00")
        default_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.weekdays_var = [i for i, day in enumerate(default_weekdays) if day in default_weekdays]

        common_frame = tk.Frame(root, padx=20, pady=10)  # Add padding to the common frame
        common_frame.grid(row=0, column=0)

        # UI elements
        
        tk.Label(common_frame, text="Username:", pady=5).grid(row=0, column=0)
        self.username_entry = tk.Entry(common_frame, textvariable=self.username_var)
        self.password_entry_grid = self.username_entry.grid(row=0, column=1, columnspan=2, sticky="ew")

        tk.Label(common_frame, text="Password:",pady=5).grid(row=1, column=0)
        self.password_entry = tk.Entry(common_frame, textvariable=self.password_var, show='*')
        self.password_entry_grid = self.password_entry.grid(row=1, column=1,columnspan=2, sticky="ew")

        tk.Label(common_frame, text="Check-in Time:",pady=5).grid(row=2, column=0)
        self.start_time_picker = TimePicker(common_frame, self.start_time_var)
        self.start_time_picker.grid(row=2, column=1)

        tk.Label(common_frame, text="End Time:",pady=5).grid(row=3, column=0)
        self.end_time_picker = TimePicker(common_frame, self.end_time_var)
        self.end_time_picker.grid(row=3, column=1)

        # Weekday checkboxes
        tk.Label(common_frame, text="Select Weekdays:", pady=5).grid(row=4, column=0, columnspan=2, sticky='w')
        self.weekday_checkboxes = []
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(weekdays):
            var = tk.IntVar(value=1 if i in self.weekdays_var else 0)
            checkbox = tk.Checkbutton(common_frame, text=day, variable=var, onvalue=1, offvalue=0, command=self.update_selected_days)
            checkbox.grid(row=i // 2 + 4, column=i % 2 +1, sticky='w')
            self.weekday_checkboxes.append((day, var))


        tk.Button(common_frame, text="Save", width=15, bg="#4CAF50", fg="white", command=self.save).grid(row=8, column=0, columnspan=3, pady=10)
        tk.Button(common_frame, text="Cancel", width=10, bg="#A9A9A9", fg="#363636", command=self.cancel).grid(row=8, column=2, columnspan=1, pady=10)


        # Calculate the center position
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 350  # Set your desired width
        window_height = 280  # Set your desired height
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Disable maximize button and set initial size
        self.root.resizable(False, False)
        geometry_string = f"{window_width}x{window_height}+{x_position}+{y_position}"
        root.geometry(geometry_string)


    def update_selected_days(self):
        selected_days = [i for i, (day, var) in enumerate(self.weekday_checkboxes) if var.get()]
        self.weekdays_var = selected_days

    
    def cancel(self):
        self.root.destroy()


    def save(self):
        if not self.username_var.get():
            show_message("Please enter a username")
            self.username_entry.focus_set()
            return
        
        if not self.password_var.get():
            show_message("Please enter a password")
            self.password_entry.focus_set()
            return

        preferences = {
            'username': self.username_var.get(),
            'password': self.password_var.get(),
            'start_time': self.start_time_var.get(),
            'end_time': self.end_time_var.get(),
            'weekdays': list(self.weekdays_var),
        }

        save_preferences(preferences)
        self.root.destroy()

    
def load_config_ui():
    root = tk.Tk()
    ConfigUI(root)
    root.mainloop()


def load_preferences(self):
    if  preference_exists():
        with open('preferences.json', 'r') as file:
            preferences = json.load(file)
            self.username = preferences.get('username', '')
            self.password = preferences.get('password', '')
            self.start_time = preferences.get('start_time', '')
            self.end_time = preferences.get('end_time', '')
            self.weekdays = preferences.get('weekdays', '')


def save_preferences(preferences):
    with open('preferences.json', 'w') as file:
        json.dump(preferences, file)

    messagebox.showinfo("Preferences Saved", "User preferences have been saved.")


