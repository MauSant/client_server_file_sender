import socket

class ClientConfig:

    MAIN_SERVER_HOST = 'HOST'
    MAIN_SERVER_PORT = 'PORT'
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 7777
    ENDRÇ = (IP,PORT)
    FORMAT = "utf-8"
    SIZE = 1024
    