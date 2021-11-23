from client import client_controller
# from cliente.interface import face
# from cliente.interface.face import interface
from interface import face
from interface.face import interface


if __name__ == '__main__':
    # action, server_host, server_port = interface()
    interface()
    
    # client_controller(
    #                   action= face.action,
    #                   file_path= face.local_arquivo,
    #                   replic_number= face.replics,
    #                  )