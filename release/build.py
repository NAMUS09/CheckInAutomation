import subprocess

# Run version_file_script.py to generate the version file
subprocess.run(['python', 'release/version_file_script.py'])

# Run the script to build the executable using PyInstaller
subprocess.run(['python', 'release/pyinstaller_script.py'])
