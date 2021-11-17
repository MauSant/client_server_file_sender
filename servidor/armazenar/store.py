import  os
import json
import	socket

<<<<<<< HEAD

=======
>>>>>>> 153aa5fd42955231ab6ba119edcc5ed37d8691e5
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
            header = mk_header()
            connect_socket.send(header)
            connect_socket.send(f)
        connect_socket.close()

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

    storage_load()
    print(file_storage[1])
    print(servers_storage[0])
