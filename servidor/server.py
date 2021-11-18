from typing import Collection, Optional, Dict, Tuple
import json
import socket
from server_config import ServerConfig  as config
from armazenar.store import add_file
from ntpath import basename as get_base_file_name
import time

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
        time.sleep(0.5)
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
        except Exception:
            socket.close()
            client_socket.close()


'''As funções a serem utilizadas no execute_action, estão aqui '''
def load_funcs():
    funcs_dict = {
        "store": store,
        "retrieve": retrieve_file
    } 
    return funcs_dict  

def accept_connection(socket:object) -> Tuple:
    #Retorna True or False E
    #ACEITA A CONEXÃO e retorna o socket do client
    try:
        client_socket, address = socket.accept()
    except Exception as e:
        print('Falha ao aceitar conexão')
        return False, None, None
    else:
        return True, client_socket, address
    

def receive_header(socket:object) -> Dict:
    serial = socket.recv(1024).decode('utf-8')
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
    elif action == 'search':
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
    file = client_socket.recv(1024).decode('utf-8')
    # file = client_socket.recv(2048)

    add_file(name=name,copies=replic_number, file=file)

    return 'Deu certo'

def retrieve_file(args: Dict) -> bytes:
    print('retrieve')
    socket = args['socket']
    action = args['action']
    keyword = args['keyword']
    pass

def send_file(header:Dict, file:bytes) -> str:
    pass

