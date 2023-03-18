from dataclasses import dataclass
from socket import socket
from threading import Lock


@dataclass
class Player:
    ip: str
    wing: socket
    controller: Lock = Lock()
    username: str = None

