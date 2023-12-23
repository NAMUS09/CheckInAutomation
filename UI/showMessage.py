import json
import tkinter as tk
from UI.config_ui import ConfigUI
from PIL import Image, ImageTk
from utils.common import resource_path 
from utils.geometry import Geometry

class MessageBox:

    def __init__(self, root, title, message):
        self.root = root
        self.root.title(title)
        
        png_path = resource_path("assets/info.png")
        
        common_frame = tk.Frame(root, padx=5, pady=3)
        common_frame.grid(row=0, column=0, sticky="nsew")

        # UI elements

        # software version
        config_json_path = resource_path("config.json")

        # Read the configuration from the JSON file
        with open(config_json_path, 'r') as config_file:
            config = json.load(config_file) 

        # return the app version from the configuration
        app_version = config.get('app_version', '1.0.0') #default value

        app_version_label = tk.Label(common_frame, text=f"Version: {app_version}", foreground="#4d5254", compound="left")
        app_version_label.grid(row=0, column=0, pady=2, padx=2, sticky="w")

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


        # Disable maximize button and set initial size
        self.root.resizable(False, False)

        # Force the window to update its geometry based on the widget sizes
        self.root.update_idletasks()


        # Bring the dialog window to the top
        root.attributes('-topmost', True)
        root.focus_force()

        geometry_string = Geometry.calculateCenter(root, self.root.winfo_reqwidth(), self.root.winfo_reqheight())
        root.geometry(geometry_string)


    def edit_config_clicked(self, event):
        self.root.destroy()
        ConfigUI.showConfigUI(True)

    
    def ok_button_clicked(self):
        self.root.destroy()
        

def show_message_edit_config(title: str, message):
    root = tk.Tk()

    path  = resource_path("assets/clock.ico")
    if path:
            root.iconbitmap(default=path)

    MessageBox(root, title, message)
    root.mainloop()

