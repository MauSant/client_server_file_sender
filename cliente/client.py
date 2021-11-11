from typing import Optional, Dict
import sockets.socket as socket_yuri
import os
# from socket import Socket
from cliente.client_config import ClientConfig  as config


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
   socket = socket_yuri.Socket()
   socket.connect(host, port)
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

def retrieve(
             socket:object,
             action:str,
             keyword:str,
             file_path:str,
             replic_number:int,
            ) -> bytes:
    print('retrieve')

    '''Não esquece de colocar o listening'''
    pass

def send_file(
              socket:object,
              action:str,
              keyword:str,
              file_path:str,
              replic_number:int
            ):
    print('send_file')

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
    response = func(**args)
    return response



