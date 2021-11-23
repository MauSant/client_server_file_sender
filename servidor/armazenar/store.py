import  os
import  json
import	socket
from time import sleep
from typing import Dict

port = ""
connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

my_dict = {'files' : [], 'servers' : []}

def storage_load():
    with open('servidor/armazenar/storage.json', 'r') as fp:
        data = json.load(fp)
    my_dict["files"] = data["files"]
    my_dict["servers"] = data["servers"]

def storage_save():
    with open('servidor/armazenar/storage.json', 'w') as fp:
        json.dump(my_dict, fp)

def load_args(
              action:str,
              file_name:str
             ):
    args = {
        'action': action,
        'file_name': file_name
    }
    return args

def load_funcs():
    funcs_dict = {
        "store": store_file,
        "add file": add_file,
        "retieve": retrieve_file,
        "erase":erase_file,
        "remove file": remove_file,
        "add host": add_host,
        "remove host": remove_host,
        "send file": send_bytes
    } 
    return funcs_dict  

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
    my_dict['files'].append(name)
    my_dict['files'].append(["servidor/armazenar/"+name])
    i = 0
    aux = my_dict['files'][-1]
    while i < copies-1:
         connect_socket.connect((my_dict['servers'][i],port))
         aux.append(my_dict['servers'][i])
         header = mk_header(load_args("store", name))
         connect_socket.send(header)
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

def retrieve_file (
                    file_name:str,
                    socket:object
                ):
    header = mk_header(load_args("send file", file_name))
    connect_socket.send(header)
    bts = b''
    while True:
        bts = connect_socket.recv(1024)
        if bts == b'ENDPOINT':
            socket.send(bts)
            break
        socket.send(bts)
        sleep(0.5)
    

def erase_file(
                file:str
            ):
    os.remove("servidor/armazenar/"+file)

def remove_file(
                 file:str
                ):
    erase_file(file)
    position = my_dict['files']
    repositories = position[file]
    header = mk_header(load_args("erase", file))
    for host in repositories:
         connect_socket.connect((host,port))
         connect_socket.send(header)
         connect_socket.close()

def add_host(
             name:str
            ):
    my_dict['servers'].append(name)

def remove_host(name:str):
    my_dict['servers'].remove(name)

def mk_header(args: Dict) -> bytes:
    header_j = json.dumps(args)
    serialized = header_j.encode('utf-8')
    
    return serialized

if __name__ == '__main__':
    pass
    # storage_load()
    # print(file_storage[1])
    # print(servers_storage[0])
