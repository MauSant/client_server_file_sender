from typing import Optional, Dict
import os
# from socket import Socket
from client_config import ClientConfig  as config


def client_controller(
                      action:str,
                      keyword: Optional[str] = None,
                      file_path: Optional[str] = None,
                      replic_number: Optional[int] = None
                      ) -> None:
    host = config.MAIN_SERVER_HOST
    port = config.MAIN_SERVER_PORT
    socket = prepare_socket(host, port)
    args = load_args(
                     socket,
                     action,
                     keyword,
                     file_path,
                     replic_number
                    )
    funcs_dict = load_funcs()
    response = execute_action(action, funcs_dict, args)

def prepare_socket(host:str, port:str):
    # socket = socket_yuri.Socket()
    # socket.connect(host, port)
    return 0
    return socket


def load_funcs():
    funcs_dict = {
        "retrieve": retrieve,
        "send_file": send_file,
        "change_replic": change_replic,
    } 
    return funcs_dict  

def load_args(
              socket:object,
              action:str,
              keyword:str,
              file_path:str,
              replic_number:int,
             ):
    args = {
        'socket': socket,
        'action': action,
        'keyword': keyword,
        'file_path': file_path,
        'replic_number': replic_number,
    }
    return args

def retrieve(args) -> bytes:
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

def change_replic(
                  socket:object,
                  action:str,
                  keyword:str,
                  file_path:str,
                  replic_number:int
                ):
    print('_change_replic')
    pass

def execute_action(
                   action:str,
                   funcs_dict: Dict,
                   args: Dict) -> str:
    func = funcs_dict[action]
    response = func(args)
    return response



