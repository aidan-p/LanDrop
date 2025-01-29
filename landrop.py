from flask import Flask, request, render_template, send_from_directory, jsonify
from infi.systray import SysTrayIcon
import threading
import os
import ctypes
from waitress import serve
from utils import get_ip, open_file_explorer, wifi_alert
import constants
import configparser

# Hides Python from taskbar
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Check for wifi_alert
config = configparser.ConfigParser()
config.read('preferences.ini')
if config.has_section('Settings') and config.has_option('Settings', 'WiFiAlert'):
    wifi_alert = config.get('Settings', 'WiFiAlert')
    if wifi_alert == 'yes':
        wifi_alert()
else:
    wifi_alert()

# Get local ip
localip = get_ip(constants.portNum)

# Initilize app
app = Flask(__name__)

# Ensure the upload folder exists
os.makedirs(constants.UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = constants.UPLOAD_FOLDER

@app.route("/")
def index():
    # Get the list of files in the uploads folder
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    if file:
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)
        return jsonify({"success": True})
    else:
        return jsonify({"success": False})

@app.route("/upload/<filename>")
def send_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Initialize system tray
def start_tray_icon():
    menu_options = ((localip, None, lambda sys_tray_icon: None), ("Send File", None, open_file_explorer),)
    systray = SysTrayIcon("./static/icon.ico", "LanDrop", menu_options)
    systray.start()

def start_local_server():
    serve(app, host="0.0.0.0", port=constants.portNum)

if __name__ == "__main__":
    # Run server
    server_thread = threading.Thread(target=start_local_server)
    server_thread.daemon = True
    server_thread.start()

    start_tray_icon()