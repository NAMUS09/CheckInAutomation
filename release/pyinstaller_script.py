import json
import subprocess

# Read the configuration from the JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


app_version = config.get('app_version', '1.0.0') #default value


# Construct the name of the executable with version
executable_name = f"{config.get('app_name')}-{app_version}"

# Construct the PyInstaller command based on the configuration
command = [
    'pyinstaller',
    '--noconsole' if config.get('noconsole') else '',
    '--onefile' if config.get('onefile') else '',
    '--clean' if config.get('clean') else '',
    f'--icon={config.get("icon")}' if config.get('icon') else '',
    f'--name={executable_name}',
    f'--version-file=versionfile.txt',
]

# Handling multiple --add-data entries
add_data = config.get("add_data")
if add_data:
    for data_entry in add_data:
        command.append(f'--add-data "{data_entry}"')

# append remaining
command.append(config.get('script_name', 'main.py'))

# Filter out empty strings from the command list
command = list(filter(None, command))

# Join the command parts into a single string
command_str = ' '.join(command)

print(command_str)

# Run the PyInstaller command
subprocess.run(command_str, shell=True)
