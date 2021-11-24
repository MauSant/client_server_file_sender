from typing import Collection, Optional, Dict, Tuple
import json
import socket
from server_config import ServerConfig  as config
from time import sleep
import os

def server_controller() -> None:
    port = config.MAIN_SERVER_PORT
    host = config.MAIN_SERVER_HOST
    socket = prepare_socket(host, port)
    server_listening(socket)
    
def prepare_socket(host:str, port:str):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    return server_socket    
    
def server_listening(socket):
    funcs_dict = load_funcs()
    socket.listen()

    while(True):
        print('esperando conexão')
        sleep(0.5)
        permission, client_socket, address = accept_connection(socket)
        if not permission:
            continue #Caso a conexão n for aceita, não precisa ler o restante do código e pula pro proximo
        print(f'Conectado a {address}')

        header = receive_header(client_socket)

        args = load_args(socket, client_socket ,header)
        try:
            response = execute_action(
                                    action=args['action'],
                                    funcs_dict=funcs_dict,
                                    args=args
                                    )
        except Exception as e:
            socket.close()
            client_socket.close()
            raise e


'''As funções a serem utilizadas no execute_action, estão aqui '''
def load_funcs():
    funcs_dict = {
        'store_inremote': store_inremote,
        'get_inremote': get_inremote,
        'erase': erase_file
    } 
    return funcs_dict  


def accept_connection(socket:object) -> Tuple:
    try:
        client_socket, address = socket.accept()
    except Exception as e:
        print('Falha ao aceitar conexão')
        return False, None, None
    else:
        return True, client_socket, address
    

def receive_header(socket:object) -> Dict:
    serial = socket.recv(config.SIZE).decode('utf-8')
    header = json.loads(serial)
    return header


def load_args(socket:object, client_socket:object, header:Dict) -> Dict:
    args = header
    args['socket'] = socket
    args['client_socket'] = client_socket
    return args


def execute_action(action:str, funcs_dict: Dict, args: Dict) -> str:
    func = funcs_dict[action]
    response = func(args)
    return response


def store_inremote(args: dict):
    print('store in remote')
    client_socket = args['client_socket']
    file_name = args['keyword']
    print('Esperando receber file')
    data = receive_file(client_socket)
    store_file(file_name, data)


def get_inremote(args: dict) -> bytes:
    file_name = args['keyword']
    main_socket = args['client_socket'] # connection between main_server and mock_server
    send_bytes(file_name, main_socket) # send file to the main_server


def receive_file(client_socket:object):
    data = b''
    bts = b''
    while True:
        print("Receiving...")
        bts = client_socket.recv(1024)
        if bts == b'ENDPOINT':
            break
        data += bts
    return data


def send_bytes(file_name: str, connect_socket: object):
    with open("servidor-mock/armazenar/"+file_name, 'rb') as file:
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


def erase_file(args: dict):
    file_name = args['keyword']
    os.remove("servidor-mock/armazenar/"+file_name)


def store_file(file_name:str, data:bytes):
    file_copy = open("servidor-mock/armazenar/"+file_name, "wb")
    file_copy.write(data)
    file_copy.close()

