from typing import Optional, Dict, Tuple
import os
import socket
from client_config import ClientConfig  as config
import json

def client_controller(
                      action:str,
                      keyword: Optional[str] = None,
                      file_path: Optional[str] = None,
                      replic_number: Optional[int] = None,
                      ) -> None:

    permission, client_socket = request_connection(config)
    if not not permission:
        raise ConnectionError('Falha na conexão, tente mais tarde')

    args = load_args(
                     client_socket,
                     action,
                     keyword,
                     file_path,
                     replic_number
                    )
    funcs_dict = load_funcs()
    response = execute_action(action, funcs_dict, args)

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
        "send": send_file
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
    action = args['action']
    keyword = args['keyword']


    
    '''Não esquece de colocar o listening'''
    pass

def send_file(args: Dict) -> None:
    print('send_file')

    client_socket = args['client_socket']
    file_path = args['file_path']
    
    header = mk_header(args)
    client_socket.sendall(header) # send header
 
    '''Isso deve funcionar para um txt, mas e se precisar mandar um pdf ou imagem? '''
    file = open(file_path, "r")
    data = file.read()
    client_socket.sendall(data) #send file
    ''' '''
    
    msg = client_socket.recv(config.SIZE).decode(config.FORMAT)
    print(f"[SERVER]: {msg}")
    

def mk_header(args: Dict) -> bytes:
    args.pop('client_socket', None) #Não precisa enviar o client socket
    header_j = json.dumps(args)
    serialized = header_j.encode(config.FORMAT)#client
    # json.loads(b.decode('utf-8'))#server
    
    return serialized

   

    





