import  os
import  json
#from servidor.server import server_listening
import	socket
from time import sleep
from typing import Dict
from server_config import ServerConfig  as config
from ntpath import basename as get_base_file_name




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
    store_file(file_name, data) #save on local (disk)
    index_files = append_index(index_files, file_name, config.MAIN_ADDRESS) # update index with main address

    index_files = send_file_toremote(replic_number, socket, file_name, index_files) #save on remote
    index_save(index_files) #register on index.json


def append_index(index_files, file_name, address) -> dict:
    try:
        index_files[file_name].append(address) #register on local(ram)
    except KeyError:# in case the key does not exists
        index_files[file_name] = [address]
    finally:
        return index_files


def send_file_toremote(
                       replic_number: int,
                       socket: object,
                       file_name:str,
                       index_files: dict
                      ) -> dict:
    
    header = mk_header({'action':'store_inremote',  'keyword': file_name})
    SERVERS_DICT = config.SERVERS_DICT

    for i in range(1,replic_number+1):
        remote_addr = SERVERS_DICT[i]
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect(remote_addr)

        remote_socket.send(header)
        sleep(0.5)
        send_bytes(file_name, remote_socket)
        
        index_files = append_index(index_files, file_name, remote_addr)
        
        remote_socket.close()

    return index_files


def send_bytes(file_name: str, connect_socket: object):
    with open("servidor/armazenar/"+file_name, 'rb') as file:
        while (True):
            bts = file.read(1024)
            if not bts:
                bts = b'ENDPOINT'
                connect_socket.send(bts)
                sleep(0.5)
                break
            connect_socket.send(bts)
            sleep(0.5)
        file.close()


def retrieve_file (file_name:str, client_socket:object):
    index_files = index_load()
    any_addr = search_file(keyword=file_name, index_files=index_files)
    if any_addr == config.MAIN_ADDRESS:
        send_bytes(file_name, client_socket)# Send directly for the client
    else:
        connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connect_socket.connect(any_addr)
        
        args = {
            'action': 'get_inremote',
            'keyword': file_name
        }

        header = mk_header(args)
        connect_socket.sendall(header)
        sleep(0.5)
        bts = b''
        while True:
            bts = connect_socket.recv(1024)
            if bts == b'ENDPOINT':
                client_socket.send(bts) # Envia direto para o client
                sleep(0.5)
                break
            client_socket.send(bts)
            sleep(0.5)


def search_file(keyword, index_files) -> list:
    try:
        list_addrs = index_files[keyword]
        any_addr = valid_addr(list_addrs)
    except KeyError:
        raise KeyError('O arquivo não está no indice')
    else:
        any_addr = (any_addr[0], any_addr[1])
        return any_addr


def valid_addr(list_addrs):
    if not list_addrs:
            raise ValueError('A lista de endereços está vazia!')
    for index in range(len(list_addrs)):
        try:
            any_valid_addr = list_addrs[index] # 0 is localhost, 1 is mock, 2 is mock2...
        except IndexError:
            continue
        else:
            return any_valid_addr


def erase_file(file:str):
    os.remove("servidor/armazenar/"+file)


def manage_storage(file_name, replic_number):
    index_files = index_load()
    list_addrs = index_files[file_name]

    i = 0
    if len(list_addrs) > replic_number & replic_number >= 0: # to reduce number of replics
        header = mk_header({'action':'erase',  'keyword': file_name})
        while len(list_addrs) > replic_number +1 :
            any_addr = list_addrs.pop(-1)
            connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            connect_socket.connect( (any_addr[0],any_addr[1]) )
            connect_socket.send(header)
            connect_socket.close()
            sleep(0.5)
    else:
        while replic_number > len(list_addrs) -1:
            SERVER_DICT = config.SERVERS_DICT
            for any_addr in SERVER_DICT.values():
                l_any_addr = [ any_addr[0],any_addr[1] ] 
                if l_any_addr  in list_addrs:
                    continue

                header = mk_header({'action':'store_inremote',  'keyword': file_name})
                connect_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connect_socket.connect(any_addr)
                connect_socket.send(header)
                sleep(0.5)
                send_bytes(file_name,connect_socket)
                index_files = append_index(index_files, file_name, l_any_addr)
                list_addrs = index_files[file_name]
                connect_socket.close()
                break
    index_save(index_files)
    

def mk_header(args: Dict) -> bytes:
    header_j = json.dumps(args)
    serialized = header_j.encode('utf-8')
    
    return serialized
