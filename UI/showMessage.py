import subprocess
import sys
from tkinter import messagebox
from packaging import version
import json
import tkinter as tk
from UI.config_ui import ConfigUI
from PIL import Image, ImageTk
from utils import  resource_path, download_latest_app, get_latest_release_version ,get_current_app_version
from utils.common import show_message
from utils.geometry import Geometry

class MessageBox:

    def __init__(self, root, title, message, showReCheckIn):
        self.root = root
        self.root.title(title)
        self.reCheckInClicked = False
        
        png_path = resource_path("assets/info.png")
        update_icon_path = resource_path("assets/update.png")
        
        common_frame = tk.Frame(root, padx=5, pady=3)
        common_frame.grid(row=0, column=0, sticky="nsew")

        # UI elements
        app_version = get_current_app_version() 
        app_version_label = tk.Label(common_frame, text=f"Version: {app_version}", foreground="#4d5254", compound="left")
        app_version_label.grid(row=0, column=0, pady=2, padx=2, sticky="w")

        # fetch latest version from github
        app_release_response = get_latest_release_version()
        self.assets_url = app_release_response.get("assets_url")
        if(version.parse(app_release_response.get("version")) < version.parse(app_version)):
            #Load the update PNG image
            update_icon = Image.open(update_icon_path)
            update_icon.thumbnail((20, 20))
            update_icon = ImageTk.PhotoImage(update_icon)            
            #label
            app_update_label = tk.Label(common_frame,image=update_icon, text=f"Update Available", foreground="#4ec43f", cursor="hand2", compound="left", padx=5)
            if update_icon:
                app_update_label.image = update_icon
            app_update_label.grid(row=0, column=0, pady=2, padx=2, sticky="s")
            app_update_label.bind("<Button-1>", self.update_available_clicked)


        # Edit Configuration Label
        edit_config_label = tk.Label(common_frame, text="Edit Configuration", foreground="blue", cursor="hand2", compound="right")
        edit_config_label.grid(row=0, column=0, pady=2, padx=2, sticky="e")
        edit_config_label.bind("<Button-1>", self.edit_config_clicked)


        #Load the PNG image
        info_icon = Image.open(png_path)
        info_icon.thumbnail((35, 35))
        info_icon = ImageTk.PhotoImage(info_icon)
        info_label = tk.Label(common_frame, image=info_icon, text=message, compound="left", padx=10)
        if info_icon:
            info_label.image = info_icon
        info_label.grid(row=2, column=0, columnspan=1, pady=2, padx=2)


        # Frame for the OK Button with a gray background
        footer_frame = tk.Frame(root, bg="#d9d9d9")
        footer_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")


        # OK Button in the frame
 
        ok_button = tk.Button(footer_frame, text = 'OK', fg = 'black', bg="white", bd=0, width=8,command=self.ok_button_clicked) 
       
        ok_button.pack(side="right", pady=8, padx=5)

        # Bind the Enter key to trigger the OK button
        root.bind('<Return>', lambda event: ok_button.invoke())

        # Set focus on the OK button
        root.after(1, lambda: ok_button.focus_set())

        if showReCheckIn:
            # Retry Check-In Button in the frame
    
            retry_button = tk.Button(footer_frame, text = 'Retry Check-In', fg = 'black', bg="white", bd=0, width=12,command=self.reCheckIn_button_clicked) 
        
            retry_button.pack(side="right", pady=8, padx=5)

            # Bind the Enter key to trigger the OK button
            root.bind('<Return>', lambda event: retry_button.invoke())

        # Disable maximize button and set initial size
        self.root.resizable(False, False)

        # Force the window to update its geometry based on the widget sizes
        self.root.update_idletasks()

        # Bring the dialog window to the top
        root.attributes('-topmost', True)
        root.focus_force()

        geometry_string = Geometry.calculateCenter(root, self.root.winfo_reqwidth(), self.root.winfo_reqheight())
        root.geometry(geometry_string)

    def update_available_clicked(self, event):
        application_exe_path = download_latest_app(self.assets_url )

        if application_exe_path is not None:
            # Show update notification
            result = messagebox.showinfo("Update Successful", "The application has been successfully updated. Click ok to restart")          
            if result:
                self.run_new_app(application_exe_path=application_exe_path)
    
    def run_new_app(self, application_exe_path):
        self.root.destroy()
        # Run the new executable
        subprocess.Popen(application_exe_path)
        self.close_program()

    def close_program(self, event=None):
        # Close the program
        sys.exit()

    def edit_config_clicked(self, event):
        self.root.destroy()
        ConfigUI.showConfigUI(True)

    def ok_button_clicked(self):
        self.root.destroy()

    def reCheckIn_button_clicked(self):
        self.reCheckInClicked = True  
        self.root.destroy()
        

def show_message_edit_config(title: str, message: str, showReCheckIn = False): 
    root = tk.Tk()

    path  = resource_path("assets/clock.ico")
    if path:
            root.iconbitmap(default=path)

    messageBox = MessageBox(root, title, message, showReCheckIn)
    root.mainloop()

    return messageBox.reCheckInClicked

