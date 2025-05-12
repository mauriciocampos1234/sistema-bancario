import json
from datetime import datetime, timedelta
import pytz

# Caminho do arquivo de persistência
ARQUIVO_DADOS = "dados_bancarios.json"

# Variáveis globais (serão carregadas/salvas no JSON)
usuarios = []
contas = []
historico = []

# Outras variáveis de operação
saldo = 0.0
limite_cheque_especial = 1000.0  # Novo recurso: limite concedido pelo banco
opcao_menu = -1

LIMITE_DEPOSITOS = 3
LIMITE_EXTRATOS = 3
LIMITE_SAQUES_DIA = 3
VALOR_MAX_SAQUE = 500

contagem_depositos = 0
contagem_extratos = 0
contagem_saques_hoje = 0
data_ultimo_saque = datetime.now(pytz.timezone("America/Sao_Paulo")).date()

depositos_pendentes = []  # temporário, não precisa salvar

# Variáveis do login
usuario_logado = None
conta_ativa = None
prox_numero_conta = 1

# --- FUNÇÕES DE PERSISTÊNCIA ---

def carregar_dados():
    global usuarios, contas, historico, prox_numero_conta
    try:
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            usuarios = dados.get("usuarios", [])
            contas = dados.get("contas", [])
            historico = dados.get("historico", [])

            # Determina o próximo número de conta disponível
            if contas:
                prox_numero_conta = max(c["numero"] for c in contas) + 1
            else:
                prox_numero_conta = 1

            print("✅ Dados carregados com sucesso.")
    except FileNotFoundError:
        print("⚠️ Arquivo de dados não encontrado. Iniciando com dados vazios.")
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")

def salvar_dados():
    dados = {
        "usuarios": usuarios,
        "contas": contas,
        "historico": historico
    }
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        print("💾 Dados salvos com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao salvar dados: {e}")

# --- FUNÇÕES AUXILIARES ---

def limpar_tela():
    print("\n" * 100)

def validar_cpf(cpf):
    return cpf.isdigit() and len(cpf) == 11

def encontrar_usuario_por_cpf(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def encontrar_conta_por_numero(numero):
    for conta in contas:
        if conta["numero"] == numero and conta["ativo"]:
            return conta
    return None

def compensar_depositos():
    """Essa função pode ser reativada depois para simular compensação real."""
    global saldo
    agora = datetime.now(pytz.timezone("America/Sao_Paulo"))
    for deposito in depositos_pendentes[:]:
        if agora >= deposito["compensacao"]:
            saldo += deposito["valor"]
            deposito["status"] = "Efetivado"
            historico.append({
                "tipo": "Depósito",
                "valor": deposito["valor"],
                "data": agora.isoformat(),
                "status": "Efetivado",
                "conta_numero": conta_ativa["numero"]
            })
            depositos_pendentes.remove(deposito)
            print(f"💰 Depósito compensado: R$ {deposito['valor']:.2f}")

# --- CADASTROS E LOGIN ---

def criar_usuario():
    print("🧾 Cadastrar novo usuário")
    nome = input("Nome completo: ")
    nascimento = input("Data de nascimento (dd/mm/yyyy): ")
    cpf = input("CPF (somente números): ").strip()
    endereco = input("Endereço (logradouro, número - bairro - cidade/sigla - cep): ")

    if not validar_cpf(cpf):
        print("❌ CPF inválido.")
        return

    if encontrar_usuario_por_cpf(cpf):
        print("⚠️ Já existe um usuário com esse CPF.")
        return

    usuarios.append({
        "nome": nome,
        "nascimento": nascimento,
        "cpf": cpf,
        "endereco": endereco
    })
    salvar_dados()
    print("✅ Usuário cadastrado com sucesso!")

def listar_usuarios():
    print("👥 Lista de usuários:")
    if not usuarios:
        print("🔍 Nenhum usuário cadastrado.")
        return
    for u in usuarios:
        print(f"{u['nome']} | CPF: {u['cpf']}")

def criar_conta_corrente():
    global prox_numero_conta
    cpf = input("Digite o CPF do usuário para vincular a conta: ")
    usuario = encontrar_usuario_por_cpf(cpf)
    if not usuario:
        print("❌ Usuário não encontrado.")
        return

    nova_conta = {
        "agencia": "0001",
        "numero": prox_numero_conta,
        "usuario_cpf": cpf,
        "ativo": True
    }

    contas.append(nova_conta)
    prox_numero_conta += 1
    salvar_dados()
    print(f"✅ Conta criada com sucesso! Número da conta: {nova_conta['numero']}")

def listar_contas():
    print("🏦 Lista de contas correntes:")
    if not contas:
        print("🔍 Nenhuma conta cadastrada.")
        return
    for c in contas:
        if c["ativo"]:
            print(f"Agência: {c['agencia']} | Conta: {c['numero']} | CPF: {c['usuario_cpf']}")

def login():
    global usuario_logado, conta_ativa
    cpf = input("Digite seu CPF para login: ")
    usuario = encontrar_usuario_por_cpf(cpf)
    if not usuario:
        print("❌ Usuário não encontrado.")
        return

    contas_do_usuario = [c for c in contas if c["usuario_cpf"] == cpf and c["ativo"]]
    if not contas_do_usuario:
        print("❌ Você não possui conta ativa.")
        return

    print("Selecione sua conta:")
    for conta in contas_do_usuario:
        print(f"Número: {conta['numero']} | Agência: {conta['agencia']}")

    numero_selecionado = int(input("Digite o número da conta desejada: "))
    conta_selecionada = encontrar_conta_por_numero(numero_selecionado)

    if not conta_selecionada or conta_selecionada not in contas_do_usuario:
        print("❌ Conta inválida ou inativa.")
        return

    usuario_logado = usuario
    conta_ativa = conta_selecionada
    print(f"🔓 Login realizado com sucesso! Bem-vindo(a), {usuario['nome']}.")

# --- OPERAÇÕES DO MENU PRINCIPAL ---

def menu_principal():
    print("\nMENU PRINCIPAL")
    print("1 - Depositar")
    print("2 - Saldo")
    print("3 - Extrato")
    print("4 - Sacar")
    print("0 - Sair")

def depositar():
    global contagem_depositos
    if contagem_depositos >= LIMITE_DEPOSITOS:
        print("⚠️ Limite máximo de depósitos excedido.")
        return

    print("📥 Você escolheu a opção Depositar!")
    valor = float(input("Digite o valor do depósito: "))

    print("Selecione o tipo de depósito:")
    print("1 - Dinheiro")
    print("2 - Cheque")
    tipo_opcao = input("Escolha uma opção (1 ou 2): ").strip()

    agora = datetime.now(pytz.timezone("America/Sao_Paulo"))
    hora = agora.hour
    compensacao = None

    if tipo_opcao == "1":
        if agora.weekday() >= 5 or hora >= 16:
            compensacao = (agora + timedelta(days=(7 - agora.weekday()) % 7 or 1)).replace(hour=11, minute=0, second=0)
        else:
            compensacao = agora.replace(hour=18, minute=0, second=0)
        print("🟢 Depósito em dinheiro agendado para compensação.")

    elif tipo_opcao == "2":
        dias_compensacao = 2
        if agora.weekday() >= 5 or hora >= 16:
            dias_compensacao += 1
        compensacao = agora + timedelta(days=dias_compensacao).replace(hour=18, minute=0, second=0)
        print("🟡 Depósito em cheque agendado para compensação (até 3 dias úteis).")

    else:
        print("❌ Opção inválida. Tente novamente.")
        return

    depositos_pendentes.append({
        "valor": valor,
        "compensacao": compensacao,
        "status": "Pendente"
    })

    historico.append({
        "tipo": "Depósito",
        "valor": valor,
        "data": agora.isoformat(),
        "status": "Pendente",
        "conta_numero": conta_ativa["numero"]
    })

    contagem_depositos += 1
    print(f"✅ Depósito de R$ {valor:.2f} agendado para {compensacao.strftime('%d/%m/%Y %H:%M')}")
    salvar_dados()

def exibir_saldo():
    global saldo, limite_cheque_especial
    print("💰 Você escolheu a opção Saldo!")
    saldo_pendente = sum(d["valor"] for d in depositos_pendentes)
    saldo_disponivel = saldo + limite_cheque_especial
    print(f"💼 Saldo disponível: R$ {saldo:.2f}")
    print(f"🕒 Depósitos pendentes: R$ {saldo_pendente:.2f}")
    print(f"💳 Limite Cheque Especial: R$ {limite_cheque_especial:.2f}")
    print(f"🏦 Saldo + Limite: R$ {saldo_disponivel:.2f}")

def exibir_extrato():
    global contagem_extratos
    if contagem_extratos >= LIMITE_EXTRATOS:
        print("⚠️ Limite de extratos excedido.")
        return

    print("📄 Você escolheu a opção Extrato!")
    print("-" * 40)

    extrato_filtrado = [h for h in historico if h["conta_numero"] == conta_ativa["numero"]]

    if not extrato_filtrado:
        print("🔍 Nenhuma operação registrada.")
    else:
        for op in sorted(extrato_filtrado, key=lambda x: x["data"]):
            data_formatada = datetime.fromisoformat(op["data"]).strftime("%d/%m/%Y %H:%M")
            print(f"{op['tipo']} | R$ {op['valor']:.2f} | {data_formatada} | {op['status']}")

    print("-" * 40)
    contagem_extratos += 1

def sacar():
    global saldo, contagem_saques_hoje, data_ultimo_saque, limite_cheque_especial
    agora = datetime.now(pytz.timezone("America/Sao_Paulo"))

    if data_ultimo_saque != agora.date():
        contagem_saques_hoje = 0
        data_ultimo_saque = agora.date()

    if contagem_saques_hoje >= LIMITE_SAQUES_DIA:
        print("⚠️ Você já realizou os 3 saques permitidos hoje.")
        return

    if agora.hour >= 22 or agora.hour < 8:
        limite_saque = (saldo + limite_cheque_especial) / 2
        print("🌙 Saques após as 22h são limitados a 50% do saldo disponível.")
    else:
        limite_saque = min(saldo + limite_cheque_especial, VALOR_MAX_SAQUE)

    print(f"💵 Seu limite de saque atual é de R$ {limite_saque:.2f}")
    valor = float(input("Digite o valor do saque: "))

    if valor <= limite_saque:
        saldo -= valor
        contagem_saques_hoje += 1
        historico.append({
            "tipo": "Saque",
            "valor": valor,
            "data": agora.isoformat(),
            "status": "Efetivado",
            "conta_numero": conta_ativa["numero"]
        })
        salvar_dados()
        print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
        print("Retire seu dinheiro na boca do caixa.")
    else:
        print("❌ Valor excede o limite permitido para saque.")
        print("Tente novamente com um valor menor.")

# --- LOOP PRINCIPAL DO SISTEMA ---

carregar_dados()  # Carrega os dados antes de começar

while True:
    if not usuario_logado:
        print("\nLOGIN")
        print("1 - Fazer login")
        print("2 - Criar usuário")
        print("3 - Criar conta corrente")
        print("4 - Listar usuários")
        print("5 - Listar contas")
        print("0 - Sair")
        opcao_login = int(input("Escolha uma opção: "))
        if opcao_login == 1:
            login()
        elif opcao_login == 2:
            criar_usuario()
        elif opcao_login == 3:
            criar_conta_corrente()
        elif opcao_login == 4:
            listar_usuarios()
        elif opcao_login == 5:
            listar_contas()
        elif opcao_login == 0:
            print("👋 Sistema encerrado. Obrigado por usar nosso banco!")
            break
        else:
            print("❌ Opção inválida.")
    else:
        # COMPENSAR DEPÓSITOS COMENTADO PARA TESTES
        # compensar_depositos()

        menu_principal()
        opcao_menu = int(input("Escolha uma opção: "))
        if opcao_menu == 1:
            depositar()
        elif opcao_menu == 2:
            exibir_saldo()
        elif opcao_menu == 3:
            exibir_extrato()
        elif opcao_menu == 4:
            sacar()
        elif opcao_menu == 0:
            print(f"👋 Até breve, {usuario_logado['nome']}!")
            usuario_logado = None
            conta_ativa = None
        else:
            print("❌ Opção inválida.")