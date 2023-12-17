import os
import tkinter as tk
from config import ConfigUI
from PIL import Image, ImageTk
from utils.geometry import Geometry

class MessageBox:

    def __init__(self, root, title, message):
        self.root = root
        self.root.title(title)

        png_path = "./assets/info.png"

        common_frame = tk.Frame(root, padx=5, pady=3)
        common_frame.grid(row=0, column=0, sticky="nsew")

        # UI elements

        # Edit Configuration Label
        edit_config_label = tk.Label(common_frame, text="Edit Configuration", foreground="blue", cursor="hand2", compound="right")
        edit_config_label.grid(row=0, column=-0, pady=2, padx=2, sticky="e")
        edit_config_label.bind("<Button-1>", self.edit_config_clicked)


        #Load the PNG image
        info_icon = Image.open(png_path)
        info_icon.thumbnail((35, 35))
        info_icon = ImageTk.PhotoImage(info_icon)
        info_label = tk.Label(common_frame, image=info_icon, text=message, compound="left", padx=10)
        info_label.image = info_icon
        info_label.grid(row=2, column=0, columnspan=1, pady=2, padx=2)


        # Frame for the OK Button with a gray background
        footer_frame = tk.Frame(root, bg="#d9d9d9")
        footer_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # OK Button in the frame
        ok_button = tk.Button(footer_frame, text = 'OK', fg = 'black', bg="white", bd=0, width=8,command=self.ok_button_clicked) 
        ok_button.pack(side="right", pady=8, padx=5)


        # Disable maximize button and set initial size
        self.root.resizable(False, False)

        # Force the window to update its geometry based on the widget sizes
        self.root.update_idletasks()


        geometry_string = Geometry.calculateCenter(root, self.root.winfo_reqwidth(), self.root.winfo_reqheight())
        root.geometry(geometry_string)


    def edit_config_clicked(self, event):
        self.root.destroy()
        ConfigUI.showConfigUI(True)

    
    def ok_button_clicked(self):
        self.root.destroy()
        

    def show_message(title: str, message):
        root = tk.Tk()

        # Set window icon
        # script_dir = os.path.dirname(os.path.abspath(__file__))
        # image_path = os.path.join(script_dir, "assets", "clock.png")
        # icon = tk.PhotoImage(file=image_path)
        # root.iconphoto(True, icon)

        MessageBox(root, title, message)
        root.mainloop()

