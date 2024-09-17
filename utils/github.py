import os
import re
import subprocess
import requests
import tkinter as tk
from tkinter import ttk
from pathlib import Path
from utils import extract_zip, get_python_executable_directory, show_message, delete_file
from utils.geometry import Geometry

# access_token = "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"
# headers = {
#     "Authorization": f"token {access_token}",
#     "Accept": "application/vnd.github.v3+json"
# }    


def get_latest_release_version():
    api_url = "https://api.github.com/repos/NAMUS09/CheckInAutomation/releases/latest"
    
    try:
        #response = requests.get(api_url, headers=headers)
        response = requests.get(api_url)
        response.raise_for_status() 
        release_data = response.json()
        return { 'status': "success", 'version':  release_data['tag_name'].lstrip('v'), 'assets_url': release_data['assets_url']}
        
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while checking GitHub release: {e}")
        return { 'status': "error" }
    
def get_assets(assets_url: str):
    try: 
        response = requests.get(assets_url, headers=headers)
        response.raise_for_status() 
        assets_data = response.json()
        response_data = assets_data[0]

        return {'name': response_data['name'], 'id': response_data['id'], 'download_url':response_data['browser_download_url'] }

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while getting download url: {e}")



def download_latest_app(assets_url: str):
    try:
        # Create a progress bar
        root = tk.Tk()
        root.title("CheckInAutomation Update")

        # progressbar
        progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
        progress.grid(column=0, row=0, columnspan=2, padx=10, pady=20)

        # label
        value_label = ttk.Label(root, text="Getting ready to download the update...")
        value_label.grid(column=0, row=1, columnspan=2, pady=5)

        # Force the window to update its geometry based on the widget sizes
        root.update_idletasks()

        # Disable maximize button and set initial size
        root.resizable(False, False)

        # Bring the dialog window to the top
        root.attributes('-topmost', True)
        root.focus_force()

        # Center the window
        geometry_string = Geometry.calculateCenter(root, root.winfo_reqwidth(), root.winfo_reqheight())
        root.geometry(geometry_string)

        # Update the window
        root.update()

        # Function to update the progress bar label
        def update_progress_label():
            if progress['value']:
                return f"Current Progress: {progress['value']}%"
            return "Current Progress: 0%"

        # Function to update the progress bar
        def update_progress(chunk_size, received_bytes, total_bytes):
            progress_value = (received_bytes / total_bytes) * 100
            progress['value'] = round(progress_value, 2)
            value_label['text'] = update_progress_label()

        assets = get_assets(assets_url)
        if assets is None:
            raise ValueError("Failed to get download information.")

        # # Get the user's downloads folder
        # downloads_folder = Path.home() / "Downloads"
        # # Construct the save path
        # save_path = os.path.join(downloads_folder, assets['name'])

        save_path = os.path.join(get_python_executable_directory(), assets['name'])

        # Start downloading
        headers["Accept"] = "application/octet-stream"
        asset_url = f"https://api.github.com/repos/NAMUS09/CheckInAutomation/releases/assets/{assets['id']}"
        download_response = requests.get(asset_url, headers=headers, stream=True)
        download_response.raise_for_status()

        # Update label text
        value_label.config(text=update_progress_label())

        # Get the total file size in bytes
        total_size = int(download_response.headers.get('content-length', 0))

        # Update progress while downloading
        received_bytes = 0
        with open(save_path, 'wb') as file:
            for chunk in download_response.iter_content(chunk_size=8192):
                file.write(chunk)
                received_bytes += len(chunk)
                update_progress(chunk_size=8192, received_bytes=received_bytes, total_bytes=total_size)
                root.update()

        def get_latest_exe(extracted_dir):
            # List the extracted files
            extracted_files = os.listdir(extracted_dir)
            
            # Filter out only checkin automation .exe files
            exe_files = [filename for filename in extracted_files if filename.startswith("CheckIn") and filename.endswith(".exe")]

            if not exe_files:
                return None

            # Get the full paths of all .exe files
            exe_files_paths = [os.path.join(extracted_dir, filename) for filename in exe_files]

            # Get the latest modified .exe file
            latest_exe = max(exe_files_paths, key=os.path.getmtime)

            return latest_exe
        
        # downloaded the latest zip file to the app_executable_directory
        # Extract the downloaded zip file        
        extracted_dir = extract_zip(save_path)
        # Delete zip file
        delete_file(save_path)
        # return latest exe file path
        return get_latest_exe(extracted_dir=extracted_dir)

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while downloading: {e}")
        show_message(title="Error", message='Download Failed!!')

    except ValueError as ve:
        print(f"Error: {ve}")
        show_message(title="Error", message='Failed to get download information.')

    finally:
        if 'root' in locals():
            root.destroy()
