from typing import Collection, Optional, Dict, Tuple
import json
import socket
from server_config import ServerConfig  as config
from armazenar.store import add_file, retrieve_file, manage_storage
from ntpath import basename as get_base_file_name
from time import sleep

#Mudança server

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
        "store": store,
        "retrieve": return_file,
        "change": change_storage
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
    args['action'] = translate_action(header)
    args['socket'] = socket
    args['client_socket'] = client_socket
    return args

def translate_action(header: Dict) -> str:
    action = header['action']
    if action == 'send':
        return 'store'
    elif action == 'retrieve':
        return 'retrieve'
    else:
        raise ValueError('Nenhuma ação é valida')

def execute_action(action:str, funcs_dict: Dict, args: Dict) -> str:
    func = funcs_dict[action]
    response = func(args)
    return response

def store(args:Dict) -> str:
    print('store')
    client_socket = args['client_socket']
    socket = args['socket']
    action = args['action']
    file_path = args['file_path']
    replic_number = args['replic_number']

    name = get_base_file_name(file_path)

    print('Esperando receber file')
    data = receive_file(client_socket)

    add_file(name=name,copies=replic_number, data=data)

    return 'Deu certo'

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

def return_file(args: Dict) -> bytes:
    print('retrieve')
    socket = args['socket']
    client_socket = args['client_socket']
    keyword = args['keyword']

    retrieve_file(keyword, client_socket)
    pass

def change_storage(args: Dict):
    keyword = args['keyword']
    amount = args ['replic_number']
    manage_storage(keyword, amount)
    pass

