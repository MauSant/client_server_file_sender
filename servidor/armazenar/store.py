import  os
import	socket


port = ""
connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

file_storage = []
servers_storage = []

def store_file(
             name:str,
             file:object
            ):
    file_copy = open(name, w)
    file_copy.write(file)
    file_copy.close()

def add_file(
             name:str,
             diretectory:str,
             copies:int,
             file:object
            ):
    os.mkdir(diretectory)
    store_file(diretectory+"/"+name, file)
    file_storage.append(name, [diretectory])
    i = 0
    while i < copies:
        connect_socket.connect((servers_storage[i],port))
        aux = file_storage[-1]
        aux.append(servers_storage[i])
        file_storage[-1] = aux
        for f in file.readlines():
            connect_socket.send(f)
        connect_socket.close()
