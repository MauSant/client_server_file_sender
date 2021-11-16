from typing import Optional, Dict
import os
import socket
from client_config import ClientConfig  as config


def client_controller(
                      action:str,
                      keyword: Optional[str] = None,
                      file_path: Optional[str] = None,
                      replic_number: Optional[int] = None,
                      ) -> None:

    request_connection(config)

    args = load_args(
                     action,
                     keyword,
                     file_path,
                     replic_number
                    )
    funcs_dict = load_funcs()
    response = execute_action(action, funcs_dict, args)

def request_connection(config) -> bool:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(config.ENDRÇ)
    except Exception:
        print(f'Endereço não conectado: {config.ENDRÇ}')
        return False
    else:
        return True

def load_args(
              action:str,
              keyword:str,
              file_path:str,
              replic_number:int,
             ):
    args = {
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

    action = args['action']
    file_path = args['file_path']
    replic_number = args['replic_number']
    data = args ['arquivo']

    
 
    file = open(file_path, "r")
    data = file.read
    
    client.send(arquivo.encode(config.FORMAT))
    msg = client.recv(config.SIZE).decode(config.FORMAT)
    print(f"[SERVER]: {msg}")
    

def mk_header():
    pass

   

    





