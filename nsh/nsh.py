from simple_term_menu import TerminalMenu
import pyrebase
import os
from pathlib import Path
from .server import ServerHub


class Nsh:
    install_dir: Path
    config_dir: Path

    def __init__(self):
        firebase_config = {  # todo, fill this out with stuff that actually works
            "apiKey": "AIzaSyB7GorzPgwHYjSV4XaJoszj98tLM4_WZpE",
            "authDomain": "projectId.firebaseapp.com",
            "databaseURL": "https://api.unitystation.org",
            "storageBucket": "projectId.appspot.com"
        }
        
        self.firebase = pyrebase.initialize_app(firebase_config)

        self.config_dir = self.get_path_from_env_or_default(
            "XDG_CONFIG_HOME", Path.home() / ".config", "nsh")
        self.install_dir = self.get_path_from_env_or_default(
            "NSH_INSTALL_DIR", Path.home() / ".local" / "nsh", "")


        self.auth = self.firebase.auth()
        self.user = self.auth.sign_in_with_email_and_password(input("email:"), input( "password:"))

    def get_path_from_env_or_default(self, env_var_name: str, backup_path: Path, suffix: Path):
        if env_var := os.getenv(env_var_name):
            return_path = Path(env_var) / suffix
        else:
            return_path = backup_path / suffix
        if not return_path.exists():
            return_path.mkdir()
        return return_path

    def run(self):
        hub = ServerHub(
            "https://api.unitystation.org/serverlist", self.install_dir)
        menu = TerminalMenu([x.name.replace("\n", " ") for x in hub.servers])
        index = menu.show()
        hub.servers[index].run(self.user["refreshToken"], self.user["localId"])
