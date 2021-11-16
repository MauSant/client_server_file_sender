from typing import Collection, Optional, Dict, Tuple
import json
# from socket import Socket
from server_config import ServerConfig  as config
from armazenar.store import add_file
from ntpath import basename as get_base_file_name


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
    #socket.listening()

    while(True):
        permission, client_socket, address = accept_connection(socket)
        if not permission:
            continue #Caso a conexão n for aceita, não precisa ler o restante do código e pula pro proximo


        header = receive_header(client_socket)

        args = load_args(socket, client_socket ,header)

        response = execute_action(
                                  action=args['action'],
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

def accept_connection(socket:object) -> Tuple:
    #Retorna True or False E
    #ACEITA A CONEXÃO e retorna o socket do client
    # client_socket, address = socket.accept()
    
    #para teste
    permission = True
    client_socket = 0
    address = 0
    return permission, client_socket, address

def receive_header(socket:object) -> Dict:
    serial = socket.recv.decode('utf-8')
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
        return 'search'
    else:
        raise ValueError('Nenhuma ação é valida')

def execute_action(action:str, funcs_dict: Dict, args: Dict) -> str:
    func = funcs_dict[action]
    response = func(args)
    return response

def store(args:Dict) -> str:
    print('send_file')
    socket = args['socket']
    action = args['action']
    file_path = args['file_path']
    replic_number = args['replic_number']

    name = get_base_file_name(file_path)

    file_storage = []
    servers_storage = []

    add_file(name=name,copies=replic_number, file='')



    return 'Deu certo'

def search(args: Dict) -> bytes:
    print('retrieve')
    socket = args['socket']
    action = args['action']
    keyword = args['keyword']
    pass



