from typing import Optional, Dict
import json
# from socket import Socket
from server_config import serverConfig  as config


def server_controller() -> None:
    port = config.MAIN_SERVER_PORT
    host = config.MAIN_SERVER_HOST
    socket = prepare_socket(host, port)
    server_listening(socket)
    
def prepare_socket(host:str, port:str):
    # socket = socket_yuri.Socket()
    # socket.connect(host, port)
    return 0
    return socket    
    

def server_listening(socket):
    funcs_dict = load_funcs()

    while(True):
        #Caso a conexão n for aceita, não precisa ler o restante do código e pula pro proximo
        if not accept_connection(socket):
            continue

        header = receive_from_connection(socket)

        args = load_args(socket,header)

        response = execute_action(
                                  action=header['action'],
                                  funcs_dict=funcs_dict,
                                  args=args
                                 )
'''As funções a serem utilizadas no execute_action, estão aqui '''
def load_funcs():
    funcs_dict = {
        "retrieve": retrieve,
        "send_file": send_file,
        "change_replic": change_replic,
        "store": store,
        "search": search
    } 
    return funcs_dict  

def accept_connection(socket:object):
    # ...
    return socket

def receive_from_connection(socket:object) -> Dict:
    '''Pseudocodigo '''
    #header_json = socket.rcv.decode
    #header = json.loads(header_json)
    header = 0
    return header

def load_args(socket:object, header:Dict) -> Dict:
    args = header
    args['socket'] = socket

def execute_action(action:str, funcs_dict: Dict, args: Dict) -> Dict:
    func = funcs_dict[action]
    response = func(args)
    return response

def change_replic(args):
    '''TALVEZZ SEJA DESNECESSARIA '''
    print('_change_replic')
    pass

def retrieve(args:Dict) -> bytes:
    print('retrieve')
    socket = args['socket']
    action = args['action']
    keyword = args['keyword']
    

    '''Não esquece de colocar o listening'''
    pass

def send_file(args: Dict) -> None:
    print('send_file')
    socket = args['socket']
    action = args['action']
    file_path = args['file_path']
    replic_number = args['replic_number']
    pass

def store(args:Dict):
    pass

def search(args:Dict):
    pass





