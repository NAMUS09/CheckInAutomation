import json
import os
import base64
import sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from tkinter import messagebox
import requests

    
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


def show_message(title, message):
    messagebox.showinfo(title, message)
    

def url_reachable(url):
    req = requests.head(url)
    return req.status_code == 200


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


