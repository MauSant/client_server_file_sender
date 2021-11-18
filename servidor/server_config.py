import socket
class ServerConfig:

    MAIN_SERVER_HOST = 'localhost'
    # MAIN_SERVER_HOST = socket.gethostbyname(socket.gethostname())
    MAIN_SERVER_PORT = 4456
    SERVERS_DICT = {
        'server1': ('host','port'),
        'server2': ('host','port'),
        'server3': ('host','port')
    }