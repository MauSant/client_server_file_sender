import socket

class ClientConfig:

    # MAIN_SERVER_HOST = 'localhost'
    # MAIN_SERVER_PORT = 4455
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4440
    ENDRÇ = ('localhost',PORT)
    FORMAT = "utf-8"
    SIZE = 1024
    