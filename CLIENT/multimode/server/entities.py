from dataclasses import dataclass
from socket import socket
from threading import Lock


@dataclass
class Player:
    ip: str
    wire: socket
    controller: Lock = Lock()
    username: str = None

    def __repr__(self) -> str:
        return f'Player {self.username}'
    
