import  os
import  json
import	socket
from time import sleep

port = ""
connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#'First',['a', 'b'],'Second',['c', 'd']
#'main','son1','son2'
my_dict = {'files' : [], 'servers' : []}

file_storage = my_dict["files"]
servers_storage = my_dict["servers"]

def storage_load():
    with open('servidor/armazenar/storage.json', 'r') as fp:
        data = json.load(fp)
    my_dict["files"] = data["files"]
    my_dict["servers"] = data["servers"]
    file_storage.append(my_dict["files"])
    servers_storage.append(my_dict["servers"])

def storage_save():
    with open('servidor/armazenar/storage.json', 'w') as fp:
        json.dump(my_dict, fp)

def store_file(
             name:str,
             data:bytes
            ):
    file_copy = open("servidor/armazenar/"+name, "wb")
    file_copy.write(data)
    file_copy.close()

def add_file(
             name:str,
             copies:int,
             data:bytes
            ):
    store_file(name, data)
    file_storage.append(name)
    file_storage.append(["servidor/armazenar/"+name])
    i = 0
    aux = file_storage[-1]
    while i < copies-1:
         connect_socket.connect((servers_storage[i],port))
         aux.append(servers_storage[i])
         send_bytes(name)
         connect_socket.close()

def send_bytes(
                file_name:str
              ):
    with open("servidor/armazenar/"+file_name, 'rb') as file:
        while (True):
            bts = file.read(1024)
            if not bts:
                bts = b'ENDPOINT'
                connect_socket.send(bts)
                break
            connect_socket.send(bts)
            sleep(0.5)
        file.close()

def erase_file(
                file:str
            ):
    os.remove("servidor/armazenar/"+file)

def remove_file(
                 file:str
                ):
    erase_file(file)
    position = file_storage.index(file)
    for host in servers_storage:
         connect_socket.connect((host,port))
         connect_socket.send("Erase file".encode)
         connect_socket.send(file.encode)
         connect_socket.close()


def add_host(
             name:str
            ):
    servers_storage.append(name)

def remove_host(name:str):
    servers_storage.remove(name)

if __name__ == '__main__':
    pass
    # storage_load()
    # print(file_storage[1])
    # print(servers_storage[0])
