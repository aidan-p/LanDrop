import configparser

config = configparser.ConfigParser()
config.read('preferences.ini')

# Read the values from the INI file
portNum = config.get('Settings', 'port')  # This will read the port number as a string
UPLOAD_FOLDER = "uploads"