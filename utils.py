import tkinter as tk
from tkinter import filedialog
from flask_socketio import SocketIO, emit
import socket
import requests
import constants
import os
import ctypes
import configparser
import webbrowser

def get_ip(portNum):
    # Get local address and define port use
    local_hostname = socket.gethostname()
    ip_addresses = socket.gethostbyname_ex(local_hostname)[2]
    filtered_ips = [ip for ip in ip_addresses if not ip.startswith("127.")]
    first_ip = filtered_ips[:1]
    return first_ip[0] + ":" + portNum

# Function to open file explorer
def open_file_explorer(icon):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    filepath = filedialog.askopenfilename()  # Open file dialog
    if filepath:
        send_file_to_website(filepath)

# Function to send the file to the local website
def send_file_to_website(filepath):
    url = "http://127.0.0.1:" + constants.portNum + "/upload"
    with open(filepath, "rb") as f:
        files = {"file": (os.path.basename(filepath), f)}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            print("Failed to upload file.")

def open_help(icon):
    webbrowser.open(f"file://{os.path.abspath("./templates/help.html")}")