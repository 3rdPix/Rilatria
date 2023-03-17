#IMPORT GENERAL
import sys 
# import socket
# import json

#IMPORT MODULES
from FrontEnd.app import Rilatria
from BackEnd.backend import load_parameters


if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = Rilatria(sys.argv)

    # parameters = load_parameters()

    # HOST = parameters['host']
    # PORT = parameters['port']

    # CLIENT = Client(HOST, PORT)

    sys.exit(app.exec_())
