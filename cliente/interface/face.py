from client import client_controller

def interface():

    global action
    action = 0
    while action != '4' :
        
        print('Bem Vindo ao YBM Storage\n Qual Operação Deseja Realizar ?\n 1-Salvar Arquivo\n 2-Buscar Arquivo\n 3-Alterar numero de Replicas\n 4-Sair')
        action = input()

        if action == '1' :
            action = 'send'
            print('Qual o path para o arquvio ?')
            local_arquivo = input()
            print('Quantas replicas desejam salvar ?')
            replics = int(input())
            client_controller(
                      action= action,
                      file_path= local_arquivo,
                      replic_number= replics,
                    )
        elif action == '2' :
            action = 'retrieve'
            print('Qual o nome do arquivo a ser buscado ?')
            nome_arquivo = input()
            client_controller(action= action, keyword=nome_arquivo)
            
        elif action == '3' :
            action = 'change'
            print('Qual o nome do arquivo a ser modificado ?')
            nome_arquivo = input()
            print('Qual o novo numero de replicas a serem salvas ?')
            replics = int(input())
            client_controller(action= action, replic_number=replics, keyword=nome_arquivo)
            

if __name__ == '__main__':

    interface()
