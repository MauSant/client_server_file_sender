from typing import Collection, Optional, Dict
import json
# from socket import Socket
from server_config import ServerConfig  as config
from armazenar.store import add_file


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
        permission, client_socket, address = accept_connection(socket)
        if not permission:
            continue #Caso a conexão n for aceita, não precisa ler o restante do código e pula pro proximo


        header = receive_header(client_socket)

        args = load_args(socket, client_socket ,header)

        response = execute_action(
                                  action=header['action'],
                                  funcs_dict=funcs_dict,
                                  args=args
                                 )

'''As funções a serem utilizadas no execute_action, estão aqui '''
def load_funcs():
    funcs_dict = {
        "change_replic": change_replic,
        "store": store,
        "search": search
    } 
    return funcs_dict  

def accept_connection(socket:object)->Tuple:
    #Retorna True or False E
    #ACEITA A CONEXÃO e retorna o socket do client
    # client_socket, address = socket.accept()
    
    #para teste
    permission = True
    client_socket = 0
    address = 0
    return permission, client_socket, address

def receive_header(socket:object) -> Dict:
    '''Pseudocodigo '''
    #header_json = socket.rcv.decode
    #header = json.loads(header_json)
    header = 0 #para testar
    return header

def load_args(socket:object, client_socket:object, header:Dict) -> Dict:
    args = header
    args['socket'] = socket
    args['client_socket'] = client_socket
    return args

def execute_action(action:str, funcs_dict: Dict, args: Dict) -> Dict:
    func = funcs_dict[action]
    response = func(args)
    return response

def change_replic(args):
    '''TALVEZZ SEJA DESNECESSARIA '''
    print('_change_replic')
    pass

def store(args:Dict) -> str:
    print('send_file')
    socket = args['socket']
    action = args['action']
    file_path = args['file_path']
    replic_number = args['replic_number']

    pass

def search(args: Dict) -> bytes:
    print('retrieve')
    socket = args['socket']
    action = args['action']
    keyword = args['keyword']
    pass



