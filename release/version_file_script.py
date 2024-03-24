import json
import pyinstaller_versionfile

# Read the configuration from the JSON file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

app_version = config.get('app_version', '1.0.0') #default value

pyinstaller_versionfile.create_versionfile(
    output_file="versionfile.txt",
    version=app_version,
    company_name="Suman Shrestha",
    file_description="CheckInAutomation",
    internal_name="CheckInAutomation",
    legal_copyright="© Suman Shrestha. All rights reserved.",
    original_filename="CheckInAutomation.exe",
    product_name="CheckInAutomation"
)