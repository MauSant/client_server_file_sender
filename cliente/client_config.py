import socket

class ClientConfig:

    IP = socket.gethostbyname(socket.gethostname())
    PORT = 4440
    ENDRÇ = ('localhost',PORT)
    FORMAT = "utf-8"
    SIZE = 1024
    