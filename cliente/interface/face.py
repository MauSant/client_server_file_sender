def interface():
    global action
    print('Bem Vindo ao YBM Storage\n Qual Operação Deseja Realizar ?\n 1-Salvar Arquivo\n 2-Buscar Arquivo\n 3-Alterar numero de Replicas')
    action = input()

    if action == '1' :
        action = 'send'
        print('Qual o path para o arquvio ?')
        global local_arquivo
        local_arquivo = input()
        print('Quantas replicas desejam salvar ?')
        global replics
        replics = input()
    elif action == '2' :
        action = 'retrieve'
        print('Qual o nome do arquivo a ser buscado ?')
        global nome_arquivo
        nome_arquivo = input()
    elif action == '3' :
        action = 'change'
        print('Qual o novo numero de replicas a serem salvas ?')
        replics = input()

interface()