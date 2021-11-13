from typing import Optional, Dict
import os
import socket
from client_config import ClientConfig  as config


def client_controller(
                      action:str,
                      keyword: Optional[str] = None,
                      file_path: Optional[str] = None,
                      replic_number: Optional[int] = None,
                      arquivo: Optional[str] = None,
                      msg: Optional[str] = None,
                      ) -> None:
    host = config.MAIN_SERVER_HOST
    port = config.MAIN_SERVER_PORT
    args = load_args(
                     action,
                     keyword,
                     file_path,
                     replic_number,
                     arquivo,
                     msg,

                    )
    funcs_dict = load_funcs()
    response = execute_action(action, funcs_dict, args)


def load_args(
              action:str,
              keyword:str,
              file_path:str,
              replic_number:int,
              arquivo:str,
              msg: str
             ):
    args = {
        'action': action,
        'keyword': keyword,
        'file_path': file_path,
        'replic_number': replic_number,
        'arquivo': arquivo,
        'msg' : msg,
    }
    return args

def load_funcs():
    funcs_dict = {
        "retrieve": retrieve,
        "send_file": send_file
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
    arquivo = args['arquivo']
    data = args ['arquivo']

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(config.ENDRÇ)

    file = open(arquivo = input)
    data = file.read
    
    client.send(arquivo.encode(config.FORMAT))
    msg = client.recv(config.SIZE).decode(config.FORMAT)
    print(f"[SERVER]: {msg}")
    

   

    





