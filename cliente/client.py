from typing import Optional, Dict
# from socket import Socket



def client_controller(
                      action:str,
                      keyword: Optional[str]= None,
                      file_path: Optional[str]= None,
                      replic_number: Optional[int]= None
                      ) -> None:
    socket = create_sockets()
    args = load_args(socket, action, keyword, file_path, replic_number)
    funcs_dict = load_funcs()
    response = execute_action(action, funcs_dict, args)

def create_sockets():
    pass

def load_funcs():
    funcs_dict = {
        "retrieve": retrieve,
        "send_file": send_file,
        "change_replic": change_replic
    } 
    return funcs_dict  

def load_args(
              socket:object,
              action:str,
              keyword:str,
              file_path:str,
              replic_number:int
             ):
    args = {
        'socket': socket,
        'action': action,
        'keyword': keyword,
        'file_path': file_path,
        'replic_number': replic_number
    }
    return args


def retrieve(
             socket:object,
             action:str,
             keyword:str,
             file_path:str,
             replic_number:int
            ) -> bytes:
    print('retrieve')
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



