import tkinter as tk
from tkinter import  StringVar
from UI.timePicker import TimePicker
from utils import  getDataPath, resource_path,decrypt_data, encrypt_data, show_message
from utils.geometry import Geometry


class ConfigUI:
    def __init__(self, root, edit: bool):
        self.root = root
        self.edit = edit
        self.saved = False
        self.cancelled = False
        title = "Configuration" if not edit else "Edit Configuration"
        self.root.title(title)

        self.alert_title = "Configuration Alert"

        # Define options for the status type
        self.status_type_options = ["On-Duty", "Work From Home", "Work From Office"]

        # Define options for the status type
        self.status_session_options = ["First Half", "Second Half", "Full Day"]

        # Variables to store user input
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.status_type_var = tk.StringVar(value=self.status_type_options[2])
        self.status_session_var = tk.StringVar(value=self.status_session_options[2])
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

        tk.Label(common_frame, text="Status Type:",pady=5).grid(row=2, column=0)
        self.status_type = tk.OptionMenu(common_frame, self.status_type_var, *self.status_type_options,command=self.on_status_type_changed)
        self.status_type_grid = self.status_type.grid(row=2, column=1,columnspan=2, sticky="ew")

        tk.Label(common_frame, text="Status Session:",pady=5).grid(row=3, column=0)
        self.status_session = tk.OptionMenu(common_frame, self.status_session_var, *self.status_session_options,command=self.on_status_session_changed)
        self.status_session_grid = self.status_session.grid(row=3, column=1,columnspan=2, sticky="ew")

        tk.Label(common_frame, text="Check-in Time:",pady=5).grid(row=4, column=0)
        self.start_time_picker = TimePicker(common_frame, self.start_time_var)
        self.start_time_picker.grid(row=4, column=1)

        tk.Label(common_frame, text="End Time:",pady=5).grid(row=5, column=0)
        self.end_time_picker = TimePicker(common_frame, self.end_time_var)
        self.end_time_picker.grid(row=5, column=1)

        # Weekday checkboxes
        tk.Label(common_frame, text="Select Weekdays:", pady=5).grid(row=6, column=0, columnspan=2, sticky='w')
        self.weekday_checkboxes = []
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(weekdays):
            var = tk.IntVar(value=1 if i in self.weekdays_var else 0)
            checkbox = tk.Checkbutton(common_frame, text=day, variable=var, onvalue=1, offvalue=0, command=self.update_selected_days)
            checkbox.grid(row=i // 2 + 6, column=i % 2 +1, sticky='w')
            self.weekday_checkboxes.append((day, var))


        # Frame for footer
        footer_frame = tk.Frame(root, bg="#d9d9d9")
        footer_frame.grid(row=1, column=0, columnspan=5, sticky="nsew")

        save_button = tk.Button(footer_frame, text = 'Save', fg = 'white', bg="#7e98de", bd=0 ,width=8,command=self.validate) 
        save_button.pack(side="right", pady=8, padx=5)

        cancel_button = tk.Button(footer_frame, text = 'Cancel', fg = '#363636', bg="white", bd=0, width=8,command=self.cancel) 
        cancel_button.pack(side="right", pady=8, padx=5)

        # Bring the dialog window to the top
        root.attributes('-topmost', True)
        root.focus_force()

        # Disable maximize button and set initial size
        self.root.resizable(False, False)

        geometry_string = Geometry.calculateCenter(root, 330,340)
        root.geometry(geometry_string)

    def on_status_type_changed(self, selection):
        self.status_type_var.set(selection)

    def on_status_session_changed(self, selection):
        self.status_session_var.set(selection)


    def update_selected_days(self):
        selected_days = [i for i, (day, var) in enumerate(self.weekday_checkboxes) if var.get()]
        self.weekdays_var = selected_days
    

    def load_preferences(self):
        data_path = getDataPath()
        
        if data_path:
            with open(data_path, 'rb') as file:
                encrypted_data = file.read()
                preferences = decrypt_data(encrypted_data)
                
            self.username_var = StringVar(value = preferences.get('username', ''))
            self.password_var = StringVar(value = preferences.get('password', ''))
            self.status_type_var = StringVar(value= preferences.get('status_type', self.status_type_options[2]))
            self.status_session_var = StringVar(value= preferences.get('status_session', self.status_session_options[2]))
            self.start_time_var = StringVar(value = preferences.get('start_time', ''))
            self.end_time_var = StringVar(value = preferences.get('end_time', ''))
            self.weekdays_var = set(preferences.get('weekdays', []))
        

    def cancel(self):
        self.cancelled = True
        self.saved = False
        self.root.destroy()


    def validate(self):
        try:
            if not self.username_var.get():
                show_message(self.alert_title,"Please enter a username")
                self.username_entry.focus_set()
                return
            
            if not self.password_var.get():
                show_message(self.alert_title,"Please enter a password")
                self.password_entry.focus_set()
                return
            
            if not self.start_time_var.get():
                show_message(self.alert_title,"Please enter check in time")
                return
            
            
            if not self.end_time_var.get():
                show_message(self.alert_title,"Please enter end time")
                return
            
            if self.weekdays_var == []:
                show_message(self.alert_title,"Please select weekdays")
                return

            self.save_preferences()
            self.saved = True

        except Exception as error:
            show_message(self.alert_title,error)

        finally:
            self.cancelled = False
            self.root.destroy()


    def save_preferences(self):
        preferences = {
            'username': self.username_var.get(),
            'password': self.password_var.get(),
            'status_type': self.status_type_var.get(),
            'status_session': self.status_session_var.get(),
            'start_time': self.start_time_var.get(),
            'end_time': self.end_time_var.get(),
            'weekdays': list(self.weekdays_var),
        }

        encoded_data = encrypt_data(preferences)

        data_path = getDataPath() 

        try:
            with open(data_path, 'wb') as file:
                file.write(encoded_data)

            show_message("Preferences Saved", "User preferences have been saved.")

        except Exception as ex:
            show_message(self.alert_title, ex)


    def showConfigUI(edit = False):
        root = tk.Tk()
        
        path  = resource_path("assets/clock.ico")
        if path:
             root.iconbitmap(default=path)
    
        config = ConfigUI(root, edit)
        root.mainloop()

        return  {"saved": config.saved, "cancelled" : config.cancelled}

    
