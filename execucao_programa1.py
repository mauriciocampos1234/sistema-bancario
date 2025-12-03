# variável menu que armazena as opções do sistema exibe para o usuário porque temos os """" para criar uma string multilinha
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """ # seta o prompt do input para o usuário

# Variáveis iniciais e Constantes
saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3 # constante que define o número máximo de saques permitidos, imutável, ou seja, 
#não deve ser alterada durante a execução do programa

# Loop principal do sistema. Está em loop(True) infinito até o usuário escolher sair
while True:

    opcao = input(menu) # variável opção que recebe um atributo de input(Uusuário escolhe a opção dejejada) e 
    #exibe o menu e aguarda a escolha do usuário

    # Estrutura condicional para tratar as opções do menu, onde cada bloco trata uma funcionalidade diferente. 
    # O == é um operador de comparação que verifica se os valores são exatamente iguais, o que em outras linguagens seria ===
    if opcao == "d":
        valor = float(input("Informe o valor do depósito: ")) # variável valor que recebe o input do usuário e converte para float

        # Estrutura condicional para verificar se o valor do depósito é maior que 0
        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.3f}\n" # Adiciona o valor do depósito ao extrato formatado com 3 casas decimais

        else:
            print("Operação falhou! O valor informado é inválido.") # Mensagem de erro caso o valor do depósito seja inválido

    elif opcao == "s":
        valor = float(input("Informe o valor do saque: ")) # variável valor que recebe o input do usuário e converte para float

        excedeu_saldo = valor > saldo # Verifica se o valor do saque é maior que o saldo disponível da variável saldo 
        #atribuida a variável criada excedeu_saldo

        excedeu_limite = valor > limite # Verifica se o valor do saque é maior que o limite permitido da variável limite 
        #atribuida a variável criada excedeu_limite

        excedeu_saques = numero_saques >= LIMITE_SAQUES # Verifica se o número de saques já atingiu o limite permitido onde foi 
        #criada a variável excedeu_saques e recebeu como atribuição a variável numero_saques para comparação entre o número de saques já realizados 
        # e o limite máximo de saques permitidos

        # Estrutura condicional para tratar as diferentes condições de saque,  onde cada condição exibe uma mensagem de erro específica
        if excedeu_saldo: 
            print("Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1

        else:
            print("Operação falhou! O valor informado é inválido.")

    # Estrutura condicional para exibir o extrato das transações realizadas
    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato) # Operador ternário que verifica se o extrato está vazio
        print(f"\nSaldo: R$ {saldo:.2f}") # Exibe o saldo formatado com 2 casas decimais
        print("==========================================")

    # Estrutura condicional para sair do sistema
    elif opcao == "q":
        break # Comando break que encerra o loop infinito e sai do sistema

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
