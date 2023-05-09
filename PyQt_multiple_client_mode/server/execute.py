import sys
from server import Server
import socket

if __name__ == "__main__":
    port: int = 1714
    host: str = socket.gethostbyname(socket.gethostname())
    server = Server(host=host, port=port)

    try:
        while True:
            input("[Press Ctrl + C to close]".center(82, "+") + "\n")
    except KeyboardInterrupt:
        print("\n\n")
        print("Shutting Down...".center(80, " "))
        print("".center(82, "-"))
        print("".center(82, "-") + "\n")
        server.server_socket.close()
        sys.exit()