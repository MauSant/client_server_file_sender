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
    file_copy = open("servidor/armazenar/"+name, "w")
    for f in file.readlines():
        file_copy.write(f)
    file_copy.close()

def add_file(
             name:str,
             copies:int,
             file:object
            ):
    store_file(name, file)
    file_storage.append(name)
    file_storage.append(["servidor/armazenar/"+name])
    i = 0
    while i < copies-1:
        connect_socket.connect((servers_storage[i],port))
        aux = file_storage[-1]
        aux.append(servers_storage[i])
        file_storage[-1] = aux
        for f in file.readlines():
            connect_socket.send(f)
        connect_socket.close()

def erase_file(
            file:str
            ):
    os.remove("servidor/armazenar/"+file)

if __name__ == '__main__':
    #arquivo = open("servidor/armazenar/teste.txt", "r")
    #add_file("testeCopia.txt", 2, arquivo)
    # erase_file("testeCopia.txt")