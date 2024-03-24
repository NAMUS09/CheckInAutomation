import os
import re
import sys
import zipfile

def get_python_executable_directory():
    """
    Get the directory containing the Python executable.

    Returns:
        str: Directory containing the Python executable.
    """
    return os.path.dirname(sys.executable)


def extract_zip(zip_file_path):
    """
    Extract a zip file to the same directory.

    Args:
        zip_file_path (str): Path to the zip file.
    """
    extract_to_path = os.path.dirname(zip_file_path)
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to_path)

    return extract_to_path

    
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def getDataPath():
    data_directory = os.path.join(os.path.expanduser("~"), ".checkInAutomation")
    
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)

    return os.path.join(data_directory, "preferences.json")


def extract_version_from_filename(filename):
    # Define a regular expression pattern to match version numbers
    pattern = r"CheckInAutomation-(\d+\.\d+\.\d+)\.exe"

    # Use regex to search for the version number in the filename
    match = re.match(pattern, filename)

    if match:
        # Extract the version number from the matched group
        version_number = match.group(1)
        return version_number
    else:
        # Return None if no version number is found in the filename
        return None


def get_old_exe_paths(current_version):
    app_dir = get_python_executable_directory()
    dir_files = os.listdir(app_dir)
    
    # Filter out only CheckIn Automation .exe files
    exe_files = [filename for filename in dir_files if filename.startswith("CheckIn") and filename.endswith(".exe")]

    if not exe_files:
        return None
    
    old_exe_files_paths = []

    # Iterate through each executable file
    for filename in exe_files:
        # Extract version from the filename
        file_version = extract_version_from_filename(filename)

        if file_version != current_version:
            old_exe_files_paths.append(os.path.join(app_dir, filename))

    return old_exe_files_paths



def delete_file(file_path):
    """
    Delete a file.

    Args:
        file_path (str): Path to the file to be deleted.
        
    Returns:
        bool: True if the file was deleted successfully, False otherwise.
    """
    try:
        os.remove(file_path)
        print("File deleted successfully.")
        return True
    except OSError as e:
        print(f"Error: {file_path} - {e.strerror}")
        return False