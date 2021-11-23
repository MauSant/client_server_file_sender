import  os
import  json
import	socket
from time import sleep
from typing import Dict
from server_config import ServerConfig  as config
from ntpath import basename as get_base_file_name


port = ""
connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def index_load():
    with open('servidor/armazenar/index.json', 'r') as fp:
        index_files = json.load(fp)
    return index_files

def index_save(index_files) -> dict:
    with open('servidor/armazenar/index.json', 'w') as fp:
        json.dump(index_files, fp)


def store_file(file_name:str, data:bytes):
    file_copy = open("servidor/armazenar/"+file_name, "wb")
    file_copy.write(data)
    file_copy.close()

def add_file(file_name:str, replic_number:int, data:bytes):
    index_files = index_load()
    store_file(file_name, data, index_files) #save on local (disk)
    index_files = append_index(index_files, file_name, config.MAIN_ADDRESS) # update index with main address

    index_files = send_file_toremote(replic_number, socket, file_name, index_files) #save on remote
    index_save(index_files) #register on index.json

def append_index(index_files, file_name, address) -> dict:
    try:
        index_files[file_name].append(address) #register on local(ram)
    except KeyError:# in case the key does not exists
        index_files[file_name] = [address]
    else:
        return index_files


def send_file_toremote(
                       replic_number: int,
                       socket: object,
                       file_name:str,
                       index_files: dict
                      ) -> dict:
    
    header = mk_header({'action':'store_inremote',  'keyword': file_name})
    SERVERS_DICT = config.SERVERS_DICT

    for i in range(replic_number):
        remote_addr = SERVERS_DICT[i]
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect(remote_addr)

        remote_socket.send(header)
        sleep(0.5)
        send_bytes(file_name)
        
        index_files = append_index(index_files, file_name, remote_addr)
        
        remote_socket.close()

    return index_files


def send_bytes(file_name: str):
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
                    client_socket:object
                ):
    ip_list_file = my_dict['files'][file_name]
    files_len = len(my_dict['files'][file_name])# Search file
    if not files_len > 0 :
        print(f'arquivo não está no index do main server {file_name}')
        return None

    server_alt_addr = ip_list_file[-1]
    connect_socket.connect((server_alt_addr, port))



    header = mk_header(load_args("send file", file_name))
    connect_socket.send(header)
    bts = b''
    while True:
        bts = connect_socket.recv(1024)
        if bts == b'ENDPOINT':
            client_socket.send(bts) # Envia direto para o client
            break
        client_socket.send(bts)
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

def manage_storage(file_name, copies):
    files = my_dict['files']
    file = files[file_name]
    i = 0
    if len(file) > copies & copies > 2:
        while i < copies:
          header = mk_header(load_args("erase", file))
          connect_socket.connect((file.pop(-1),port))
          connect_socket.send(header)
          connect_socket.close()
    else:
        while i < copies-len(file) & copies < len(my_dict['servers']):
          header = mk_header(load_args("store", file))
          connect_socket.connect((my_dict['servers'][-i],port))
          connect_socket.send(header)
          send_bytes(file_name)
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
