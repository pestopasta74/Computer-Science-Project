# This module creates a json file with default settings and should be run when the program is first started.

import json
import os

# Create json file with default settings
def create_default_settings():
    settings = {
        "Font": "Arial",
        "Font size" : 12,
        "Color mode": "normal",
        "Volume": 50,
        "Icon size": 50,
    }
    with open("settings.json", "w") as file:
        json.dump(settings, file)

# Check if the settings file exists
if not os.path.exists("settings.json"):
    create_default_settings()
    print("Default settings created.")