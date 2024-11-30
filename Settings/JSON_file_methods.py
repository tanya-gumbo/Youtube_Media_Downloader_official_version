import sys
import os
import json


def read_json_file_path():
    """Reads from the settings json file"""
    app_settings_file_path = get_settings_path()
    try:
        with open(app_settings_file_path, 'r') as file:
            data = json.load(file)
            file_path = data['file_path']
            return file_path
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None


def update_json_file_path(file_path):
    """Updates data in the settings json file"""
    app_settings_file_path = get_settings_path()

    # Read the JSON file
    try:
        with open(app_settings_file_path, 'r') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        data = {}  # Start with an empty dict if the file does not exist or is empty

    # Update the values (for example, increment the download counter)
    data['file_path'] = file_path

    # Write the updated data back to the JSON file
    try:
        with open(app_settings_file_path, 'w') as file:
            json.dump(data, file, indent=4)
    except Exception as z:
        print(f"Error writing JSON file: {z}")

def get_settings_path():
    """Return the path to the settings JSON file."""
    if hasattr(sys, "_MEIPASS"):
        # Use resource_path when running in a bundled app
        file_path = os.path.join(sys._MEIPASS,'Settings', 'app_settings.json')
        return file_path
    else:
        # Use regular path for development mode
        return os.path.join("Settings", "app_settings.json")


