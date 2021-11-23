import socket
class ServerConfig:

    MAIN_SERVER_HOST = 'localhost'
    # MAIN_SERVER_HOST = socket.gethostbyname(socket.gethostname())
    MAIN_SERVER_PORT = 4440
    MAIN_ADDRESS = ('localhost',4440)
    SIZE = 1024
    SERVERS_DICT = {
        1: ('localhost',4491),# server main
        2: ('localhost',4492),
        3: ('localhost',4493)
    }