from client import client_controller

if __name__ == '__main__':
    # action, server_host, server_port = interface()
    
    client_controller(
                      action='send',
                      file_path='BD_client/test.txt',
                      replic_number=2
                     )