import tkinter as tk
from tkinter import  ttk

class TimePicker(tk.Frame):
    def __init__(self, master=None, time=None, **kwargs):
        super().__init__(master, **kwargs)
        self.time = time
        self.create_widgets()

    def validate_input(self, value, action):
        # This function is called on every key press in the Spinbox
        if action == '1':  # Action code 1 corresponds to an insertion
            return value.isdigit() or value == ''
        return True  # Allow other actions (deletions, etc.)

    def create_widgets(self):
        time_var = self.time.get() if self.time else ""
        if time_var:
            hours, minutes = map(int, time_var.split(':'))
        else:
            hours, minutes = 0, 0

        # Create StringVar for hours and minutes
        self.hour_var = tk.StringVar(value=f"{hours:02d}")
        self.minute_var = tk.StringVar(value=f"{minutes:02d}")

        validate_cmd = self.register(self.validate_input)

        self.hour_spinbox = ttk.Spinbox(
            self,
            from_=0,
            to=23,
            textvariable=self.hour_var,
            validate='key',
            validatecommand=(validate_cmd, '%P', '%d'),
            width=5,
            command=self.update_time
        )

        self.minute_spinbox = ttk.Spinbox(
            self,
            from_=0,
            to=59,
            textvariable=self.minute_var,
            validate='key',
            validatecommand=(validate_cmd, '%P', '%d'),
            width=5,
            command=self.update_time
        )

        self.hour_spinbox.grid(row=0, column=0, padx=5)
        tk.Label(self, text=":", font=('Helvetica', 12)).grid(row=0, column=1)
        self.minute_spinbox.grid(row=0, column=2, padx=5)

    def update_time(self):
        # You can perform additional logic here if needed
        hours = int(self.hour_var.get())
        minutes = int(self.minute_var.get())

        # Update the original input time
        self.time.set(f"{hours:02d}:{minutes:02d}")
