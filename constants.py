import configparser
import ctypes

def wifi_alert():
    result = ctypes.windll.user32.MessageBoxW(0, "Transmitting data through an unsecure WiFi network can allow other individuals to intercept your data. Would you like to proceed?", "ALERT", 0x4 | 0x20)
    if result == 7:
        exit()
    else:
        result2 = ctypes.windll.user32.MessageBoxW(0, "Would you like to disable this alert?", "ALERT", 0x4 | 0x20)
        if result2 == 6:
            # Check if the section exists, otherwise create it
            if not config.has_section('Settings'):
                config.add_section('Settings')

            # Write "WiFiAlert = no" to the section
            config.set('Settings', 'WiFiAlert', 'no')

            # Save the file
            with open('preferences.ini', 'w') as configfile:
                config.write(configfile)

config = configparser.ConfigParser()
config.read('preferences.ini')

# Check for wifi_alert
config = configparser.ConfigParser()
config.read('preferences.ini')
if config.has_section('Settings') and config.has_option('Settings', 'WiFiAlert'):
    wifi_alert_setting = config.get('Settings', 'WiFiAlert')
    if wifi_alert_setting == 'yes':
        wifi_alert()
else:
    wifi_alert()

if not config.has_section('Settings'):
    config.add_section('Settings')
if not config.has_option('Settings', 'Port'):
    config.set("Settings", "Port", "62333")
    with open('preferences.ini', 'w') as configfile:
        config.write(configfile)

# Read the values from the INI file
portNum = config.get('Settings', 'port')  # This will read the port number as a string
UPLOAD_FOLDER = "uploads"
