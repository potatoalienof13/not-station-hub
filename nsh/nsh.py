import simple_term_menu
import pyrebase
import os
from pathlib import Path


def create_firebase():
    config = {
        "apiKey": "AIzaSyB7GorzPgwHYjSV4XaJoszj98tLM4_WZpE",
        "authDomain": "api.unitystation.org",
    }
    return pyrebase.initialize_app(config)
files_path_var = os.getenv("NSH_FILES_DIR")
if(files_path_var is not None):
    files_directory = Path(files_path_var)
else:
    files_directory = Path(os.getenv("HOME") + "/.local/nsh")

if(not files_directory.exists()):
    os.mkdir(files_directory)

fb = create_firebase()



menu = simple_term_menu.TerminalMenu(options)
choice = menu.show()
print(choice)
print(input("login"))


