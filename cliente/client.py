from typing import Optional, Dict, Tuple
import os
import socket
from client_config import ClientConfig  as config
import json
from time import sleep


def client_controller(
                      action:str,
                      keyword: Optional[str] = None,
                      file_path: Optional[str] = None,
                      replic_number: Optional[int] = None,
) -> None:

    permission, client_socket = request_connection(config)
    if not permission:
        raise ConnectionError('Falha na conexão, tente mais tarde')

    args = load_args(
                     client_socket,
                     action,
                     keyword,
                     file_path,
                     replic_number
                    )
    funcs_dict = load_funcs()
    try:
        response = execute_action(action, funcs_dict, args)
    except Exception as e:
        print(e)
        socket.close()
        

def request_connection(config) -> Tuple:
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(config.ENDRÇ)
    except Exception:
        print(f'Endereço não conectado: {config.ENDRÇ}')
        return False, None
    else:
        return True, client_socket


def load_args(
              client_socket:object,
              action:str,
              keyword:str,
              file_path:str,
              replic_number:int,
             ):
    args = {
        'client_socket':client_socket,
        'action': action,
        'keyword': keyword,
        'file_path': file_path,
        'replic_number': replic_number,
    }
    return args


def load_funcs():
    funcs_dict = {
        "retrieve": retrieve,
        "send": send_file,
        "change": manage_storage
    } 
    return funcs_dict  


def execute_action(
                   action:str,
                   funcs_dict: Dict,
                   args: Dict) -> str:
    func = funcs_dict[action]
    response = func(args)
    return response


def retrieve(args: Dict) -> bytes:
    print('retrieve')
    client_socket = args['client_socket']
    keyword = args['keyword']


    header = mk_header(args)
    client_socket.sendall(header) # send header
    print('Retrieve sent header')
    
    data = receive_byte(client_socket)
    file_copy = open("cliente/BD_client/"+keyword, "wb")
    file_copy.write(data)
    file_copy.close()

    '''Não esquece de colocar o listening'''
    pass


def send_file(args: Dict) -> None:
    print('send_file')

    client_socket = args['client_socket']
    file_path = args['file_path']
    
    header = mk_header(args)
    client_socket.sendall(header) # send header
    sleep(0.5)

    send_bytes(client_socket, file_path)
    # #Fazer funcao
    # with open(file_path, 'rb') as file:
    #     while (True):
    #         print ('Sending...')
    #         bts = file.read(config.SIZE)
    #         if not bts:
    #             bts = b'ENDPOINT'
    #             client_socket.send(bts)
    #             break
    #         client_socket.send(bts)
    #         sleep(0.5)
            
    client_socket.close()
    # msg = client_socket.recv(config.SIZE).decode(config.FORMAT)
    # print(f"[SERVER]: {msg}")
    

def send_bytes(socket: object, file_path:str):
    with open(file_path, 'rb') as file:
        while (True):
            print ('Sending...')
            bts = file.read(config.SIZE)
            if not bts:
                bts = b'ENDPOINT'
                socket.send(bts)
                break
            socket.send(bts)
            sleep(0.5)
        
        print(f'Sent.')

def manage_storage(args:Dict):
    print('change_amount')

    client_socket = args['client_socket']
    
    header = mk_header(args)
    client_socket.sendall(header) # send header
    sleep(0.5)
    client_socket.close()

def mk_header(args: Dict) -> bytes:
    args.pop('client_socket', None) #Não precisa enviar o client socket
    header_j = json.dumps(args)
    serialized = header_j.encode(config.FORMAT)#client
    # json.loads(b.decode('utf-8'))#server
    
    return serialized

   
def receive_byte(client_socket:object) -> bytes:
    data = b''
    bts = b''
    while True:
        print("Receiving...")
        bts = client_socket.recv(1024)
        if bts == b'ENDPOINT':
            break
        data += bts
    return data

    





