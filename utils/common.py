import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tkinter import messagebox
import requests
from requests.exceptions import RequestException, ConnectionError

from utils.os import resource_path


def show_message(title, message):
    messagebox.showinfo(title, message)
    

def url_reachable(url):
    try:
        req = requests.head(url)
        return req.status_code == 200
    except ConnectionError as e:
        print(f"Connection Error: {e}")
        return False
    except RequestException as e:
        print(f"Request Exception: {e}")
        return False
    

def get_cipher_suite():
    # Passphrase to derive the key
    passphrase = b"1x$P@ssw0rd_5ecuR3!"

    # Derive a key from the passphrase using PBKDF2
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"&CheckInAutom@ti0n#%*",
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase))

     # Initialize and return the Fernet cipher with the derived key
    return  Fernet(key)


def get_current_app_version():
    # software version
    config_json_path = resource_path("config.json")

    # Read the configuration from the JSON file
    with open(config_json_path, 'r') as config_file:
        config = json.load(config_file) 

    # return the app version from the configuration
    return config.get('app_version', '1.0.0')


def encrypt_data(data: dict[str,any]):
    json_data = json.dumps(data)

    cipher_suite = get_cipher_suite()

    return cipher_suite.encrypt(json_data.encode())

def decrypt_data(encrypted_data: bytes) -> dict[str, any]:
    cipher_suite = get_cipher_suite()

    # Decrypt the data
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()

    parsed_json = json.loads(decrypted_data)

    return parsed_json


