import json
import os
import sys
import tkinter as tk
from tkinter import  StringVar, messagebox
from timePicker import TimePicker
from utils.geometry import Geometry
from utils.common import getIconPath, getDataPath


def show_message(message):
    messagebox.showinfo("Configuration Alert", message)


def preference_exists():
        script_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        data_path = os.path.join(script_dir, "data", "preferences.json") 
        return os.path.exists(data_path)
        # return os.path.exists('preferences.json')


class ConfigUI:
    def __init__(self, root, edit: bool):
        self.root = root
        self.edit = edit
        title = "Configuration" if not edit else "Edit Configuration"
        self.root.title(title)

        # Variables to store user input
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.start_time_var = tk.StringVar(value="09:00")
        self.end_time_var = tk.StringVar(value="11:00")
        default_weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        self.weekdays_var = [i for i, day in enumerate(default_weekdays) if day in default_weekdays]

        if edit:
            self.load_preferences()


        common_frame = tk.Frame(root, padx=20, pady=10)  # Add padding to the common frame
        common_frame.grid(row=0, column=0)

        # UI elements
        
        tk.Label(common_frame, text="Username:", pady=5).grid(row=0, column=0)
        self.username_entry = tk.Entry(common_frame, textvariable=self.username_var)
        self.password_entry_grid = self.username_entry.grid(row=0, column=1, columnspan=2, sticky="ew")
        self.username_entry.focus_set()

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


        # Frame for footer
        footer_frame = tk.Frame(root, bg="#d9d9d9")
        footer_frame.grid(row=1, column=0, columnspan=5, sticky="nsew")

        save_button = tk.Button(footer_frame, text = 'Save', fg = 'white', bg="#7e98de", bd=0 ,width=8,command=self.save) 
        save_button.pack(side="right", pady=8, padx=5)

        cancel_button = tk.Button(footer_frame, text = 'Cancel', fg = '#363636', bg="white", bd=0, width=8,command=self.cancel) 
        cancel_button.pack(side="right", pady=8, padx=5)


        # Disable maximize button and set initial size
        self.root.resizable(False, False)
        geometry_string = Geometry.calculateCenter(root, 330,280)
        root.geometry(geometry_string)



    def update_selected_days(self):
        selected_days = [i for i, (day, var) in enumerate(self.weekday_checkboxes) if var.get()]
        self.weekdays_var = selected_days
    

    def load_preferences(self):
        if  preference_exists():
            script_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
            data_path = os.path.join(script_dir, "data", "preferences.json") 
            with open(data_path, 'r') as file:
                preferences = json.load(file)
                self.username_var = StringVar(value = preferences.get('username', ''))
                self.password_var = StringVar(value = preferences.get('password', ''))
                self.start_time_var = StringVar(value = preferences.get('start_time', ''))
                self.end_time_var = StringVar(value = preferences.get('end_time', ''))
                self.weekdays_var = set(preferences.get('weekdays', []))

    
    def cancel(self):
        self.root.destroy()


    def save(self):
        try:
            if not self.username_var.get():
                show_message("Please enter a username")
                self.username_entry.focus_set()
                return
            
            if not self.password_var.get():
                show_message("Please enter a password")
                self.password_entry.focus_set()
                return
            
            if not self.start_time_var.get():
                show_message("Please enter check in time")
                return
            
            
            if not self.end_time_var.get():
                show_message("Please enter end time")
                return
            
            if self.weekdays_var == []:
                show_message("Please select weekdays")
                return

            preferences = {
                'username': self.username_var.get(),
                'password': self.password_var.get(),
                'start_time': self.start_time_var.get(),
                'end_time': self.end_time_var.get(),
                'weekdays': list(self.weekdays_var),
            }

            self.save_preferences(preferences)

        except Exception as error:
            show_message(error)

        finally:
            self.root.destroy()


    def save_preferences(self,preferences):
        script_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        data_directory = os.path.join(script_dir, "data")

        if not os.path.exists(data_directory):
            os.makedirs(data_directory)

        data_path = os.path.join(script_dir, "data", "preferences.json") 
        
        with open(data_path, 'w') as file:
            json.dump(preferences, file)

        messagebox.showinfo("Preferences Saved", "User preferences have been saved.")
    
    def showConfigUI(edit = False):
        root = tk.Tk()
        
        path  = getIconPath()
        if path:
             root.iconbitmap(default=path)
    
        ConfigUI(root, edit)
        root.mainloop()

    
