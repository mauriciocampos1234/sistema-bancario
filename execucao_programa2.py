import textwrap # Importa o módulo textwrap para manipulação de strings multilinha

# Função de exibição do menu e criando a interface do usuário com a variável menu que recebe uma string formatada """(Várias linhas)"""
# \n no início da string para pular uma linha antes do menu ser exibido
#\t para tabulação, ou seja, um espaço maior entre o texto e a opção.
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """ # O símbolo => indica onde o usuário deve digitar sua opção
    return input(textwrap.dedent(menu)) # textwrap.dedent() remove a indentação desnecessária da string formatada da variável menu

# Função para realizar depósitos
def depositar(saldo, valor, extrato, /): # O / indica que os parâmetros antes dele são posicionais
    if valor > 0: # Verifica se o valor do depósito é maior que zero
        saldo += valor # Adiciona o valor ao saldo
        extrato += f"Depósito:\tR$ {valor:.2f}\n" # Adiciona uma linha ao extrato com o valor do depósito formatado com duas casas decimais
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@") # Mensagem de erro para valor inválido, 
        #uso de @@@ para destacar a mensagem

    return saldo, extrato # Retorna o saldo atualizado e o extrato

# Função para realizar saques
# Função com parâmetros nomeados obrigatórios usando *, ou seja, os argumentos devem ser passados com o nome do parâmetro
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques): # Parâmetros nomeados obrigatórios
    excedeu_saldo = valor > saldo # Verifica se o valor do saque excede o saldo disponível
    excedeu_limite = valor > limite # Verifica se o valor do saque excede o limite por saque
    excedeu_saques = numero_saques >= limite_saques # Verifica se o número de saques já realizados excede o limite de saques permitidos

    # Verifica as condições de falha do saque e exibe mensagens apropriadas
    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    # Se todas as condições forem atendidas, realiza o saque
    elif valor > 0: # Verifica se o valor do saque é maior que zero
        saldo -= valor # Subtrai o valor do saldo
        extrato += f"Saque:\t\tR$ {valor:.2f}\n" # Adiciona uma linha ao extrato com o valor do saque formatado com duas casas decimais
        numero_saques += 1 # Incrementa o número de saques realizados
        print("\n=== Saque realizado com sucesso! ===")

    # Se o valor do saque for inválido (menor ou igual a zero)
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    return saldo, extrato # Retorna o saldo atualizado e o extrato

# Função para exibir o extrato
# Parâmetros posicionais obrigatórios antes do / e parâmetros nomeados obrigatórios após o *
def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato) # Exibe mensagem se o extrato estiver vazio, 
    #caso contrário exibe o extrato
    print(f"\nSaldo:\t\tR$ {saldo:.2f}") # Exibe o saldo formatado com duas casas decimais
    print("==========================================")

# Função para criar um novo usuário
# Recebe a lista de usuários como parâmetro
# Solicita os dados do usuário via input
# Verifica se o usuário já existe chamando a função filtrar_usuario() passando o CPF e a lista de usuários
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente número): ") # Solicita o CPF do usuário
    usuario = filtrar_usuario(cpf, usuarios) # Verifica se já existe um usuário com o CPF informado. filtrar_usuario é chamada 
    #para buscar o usuário na lista de usuários

    # Se o usuário já existir, exibe uma mensagem de erro e retorna
    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ") # Solicita o nome completo do usuário
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ") # Solicita a data de nascimento do usuário
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ") # Solicita o endereço do usuário

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}) # Adiciona o novo usuário 
    #à lista de usuários usando um dicionário com os dados fornecidos e a função append() que adiciona o dicionário à lista

    print("=== Usuário criado com sucesso! ===")

# Função para filtrar um usuário pelo CPF
# Retorna o usuário se encontrado, caso contrário retorna None
# Recebe o CPF e a lista de usuários como parâmetros
def filtrar_usuario(cpf, usuarios):
    # Lista de usuários filtrados pelo CPF usando list comprehension
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf] # Filtra a lista de usuários para encontrar 
    #o usuário com o CPF correspondente
    return usuarios_filtrados[0] if usuarios_filtrados else None # Retorna o primeiro usuário encontrado ou None se a lista estiver vazia

# Função para criar uma nova conta bancária
# Recebe a agência, número da conta e a lista de usuários como parâmetros
# Solicita o CPF do usuário via input e verifica se o usuário existe chamando a função filtrar_usuario()
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    # Se o usuário for encontrado, cria a conta e exibe uma mensagem de sucesso
    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario} # Retorna um dicionário representando a conta com agência,
        #número da conta e dados do usuário. Chama a função criar_conta() que cria a conta e retorna o dicionário que segnifica chave-valor

    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@") # Mensagem de erro se o usuário não for encontrado

# Função para listar todas as contas bancárias
# Recebe a lista de contas como parâmetro
# Itera sobre a lista de contas e exibe os detalhes de cada conta formatados
def listar_contas(contas):
    # for conta in contas: sigifnica que para cada conta na lista de contas, execute o bloco de código indentado abaixo
    for conta in contas:
        # String multilinha formatada com os detalhes da conta
        linha = f"""\ 
            
            Agência:\t{conta['agencia']} 
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

# Função principal do sistema bancário com todas as funcionalidades
def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []

    # Loop infinito para exibir o menu e processar as opções do usuário
    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))

            # Chama a função sacar() com parâmetros nomeados (Chave-valor dos argumentos passados)
            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1 # Gera o número da conta com base na quantidade de contas existentes, 
            #len() retorna o tamanho da lista contas
            conta = criar_conta(AGENCIA, numero_conta, usuarios) # Chama a função criar_conta() para criar uma nova conta

            # Se a conta for criada com sucesso, adiciona à lista de contas
            if conta:
                contas.append(conta) # Adiciona a nova conta à lista de contas usando a função append()

        elif opcao == "lc":
            listar_contas(contas) # Chama a função listar_contas() para exibir todas as contas bancárias

        elif opcao == "q":
            break # Sai do loop e encerra o programa

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


main() # Executa a função principal do sistema bancário
