import json
import requests
import wget
from zipfile import ZipFile
import os
from pathlib import Path


class Server:
    name: str
    fork: str
    version: str
    map: str
    gamemode: str
    time: str
    players: int
    fps: int
    ip: str
    port: str
    download_linux: str

    def __init__(self, info, install_directory: Path):
        self.update(info)
        self.install_location = Path(
            install_directory) / self.fork / str(self.version)
        self.binary_path = self.install_location / 'Unitystation'

    def update(self, info):
        self.name = info["ServerName"]
        self.fork = info["ForkName"]
        self.version = info["BuildVersion"]
        self.map = info["CurrentMap"]
        self.gamemode = info["GameMode"]
        self.time = info["IngameTime"]
        self.players = info["PlayerCount"]
        self.fps = info["fps"]
        self.ip = info["ServerIP"]
        self.port = info["ServerPort"]
        self.download_linux = info["LinuxDownload"]

    def install_build(self):

        if not self.install_location.exists():
            self.install_location.mkdir(parents=True)
        downloaded_path = self.install_location / 'install.zip'
        wget.download(self.download_linux, out=str(downloaded_path))
        with ZipFile(downloaded_path, 'r') as zip_us:
            print("attempting to extract")
            zip_us.extractall(path=self.install_location)
            print("extracting done")
        self.binary_path.chmod(744)

    def run(self, firebase_refresh_token, uid):
        if not self.binary_path.exists():
            self.install_build()
        os.chdir(self.install_location)  # todo: sandbox with firejail

        if firebase_refresh_token != "" and uid != "":
            os.system(
                f"./Unitystation --server {self.ip} --port {self.port} --refreshtoken {firebase_refresh_token} --uid {uid}")
        else:
            os.system(
                "./Unitystation --server {self.ip} --port {self.port}")


class ServerHub:

    servers = []

    def __init__(self, hub_url, install_directory: Path):
        opened_url = requests.get(hub_url)
        if opened_url.status_code == 200:
            server_list = opened_url.json()
        else:
            throw("Failed to contact hub")
            exit(-1)

        for i in server_list["servers"]:
            self.servers.append(Server(i, install_directory))
