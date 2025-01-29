from flask import Flask, request, render_template, send_from_directory, jsonify
from flask_socketio import SocketIO, emit
import os
from infi.systray import SysTrayIcon
import threading
import tkinter as tk
from tkinter import filedialog
import requests
import ctypes
import socket
from waitress import serve

# Get local address
local_hostname = socket.gethostname()
ip_addresses = socket.gethostbyname_ex(local_hostname)[2]
filtered_ips = [ip for ip in ip_addresses if not ip.startswith("127.")]
first_ip = filtered_ips[:1]
localip = first_ip[0] + ":5000"

# Hides Python from taskbar
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Flask and upload setup
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    # Get the list of files in the uploads folder
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False})

@app.route('/upload/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Function to open file explorer
def open_file_explorer(icon):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    filepath = filedialog.askopenfilename()  # Open file dialog
    if filepath:
        send_file_to_website(filepath)

# Function to send the file to the local website
def send_file_to_website(filepath):
    url = 'http://127.0.0.1:5000/upload'
    with open(filepath, 'rb') as f:
        files = {'file': (os.path.basename(filepath), f)}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            print("File uploaded successfully.")
        else:
            print("Failed to upload file.")

# Initialize system tray
def start_tray_icon():
    menu_options = ((localip, None, lambda sys_tray_icon: None), ("Send File", None, open_file_explorer),)
    systray = SysTrayIcon("./static/icon.ico", "TransferThroughPython", menu_options)
    systray.start()

def start_local_server():
    serve(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Run server
    server_thread = threading.Thread(target=start_local_server)
    server_thread.daemon = True
    server_thread.start()

    start_tray_icon()