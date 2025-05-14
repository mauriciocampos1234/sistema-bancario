import json
from datetime import datetime, timedelta
import pytz


# Caminho do arquivo de persistência
ARQUIVO_DADOS = "dados_bancarios.json"


class Usuario:
    def __init__(self, nome, nascimento, cpf, endereco):
        self.nome = nome
        self.nascimento = nascimento
        self.cpf = cpf
        self.endereco = endereco

    def to_dict(self):
        return {
            "nome": self.nome,
            "nascimento": self.nascimento,
            "cpf": self.cpf,
            "endereco": self.endereco
        }

    @staticmethod
    def from_dict(data):
        return Usuario(**data)


class Conta:
    AGENCIA_PADRAO = "0001"

    def __init__(self, numero, usuario_cpf):
        self.numero = numero
        self.agencia = self.AGENCIA_PADRAO
        self.usuario_cpf = usuario_cpf
        self.ativo = True

    def to_dict(self):
        return {
            "numero": self.numero,
            "agencia": self.agencia,
            "usuario_cpf": self.usuario_cpf,
            "ativo": self.ativo
        }

    @staticmethod
    def from_dict(data):
        conta = Conta(data["numero"], data["usuario_cpf"])
        conta.agencia = data["agencia"]
        conta.ativo = data["ativo"]
        return conta


class Historico:
    def __init__(self):
        self.registros = []

    def adicionar_registro(self, tipo, valor, status, conta_numero):
        registro = {
            "tipo": tipo,
            "valor": valor,
            "data": datetime.now(pytz.timezone("America/Sao_Paulo")).isoformat(),
            "status": status,
            "conta_numero": conta_numero
        }
        self.registros.append(registro)

    def filtrar_por_conta(self, conta_numero):
        return [r for r in self.registros if r["conta_numero"] == conta_numero]

    def to_dict(self):
        return self.registros

    def carregar_de_dict(self, registros):
        self.registros = registros


class Banco:
    LIMITE_SAQUES = 3
    VALOR_MAX_SAQUE = 500
    LIMITE_CHEQUE_ESPECIAL = 1000.0

    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.historico = Historico()
        self.saldo = 0.0
        self.contagem_saques_hoje = 0
        self.data_ultimo_saque = datetime.now(pytz.timezone("America/Sao_Paulo")).date()
        self.usuario_logado = None
        self.conta_ativa = None
        self.prox_numero_conta = 1

    def carregar_dados(self):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                self.usuarios = [Usuario.from_dict(u) for u in dados.get("usuarios", [])]
                self.contas = [Conta.from_dict(c) for c in dados.get("contas", [])]
                self.historico.carregar_de_dict(dados.get("historico", []))

                if self.contas:
                    self.prox_numero_conta = max(c.numero for c in self.contas) + 1
                print("✅ Dados carregados com sucesso.")
        except FileNotFoundError:
            print("⚠️ Arquivo de dados não encontrado. Iniciando com dados vazios.")

    def salvar_dados(self):
        dados = {
            "usuarios": [u.to_dict() for u in self.usuarios],
            "contas": [c.to_dict() for c in self.contas],
            "historico": self.historico.registros
        }
        try:
            with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"❌ Erro ao salvar dados: {e}")

    def validar_cpf(self, cpf):
        return cpf.isdigit() and len(cpf) == 11

    def encontrar_usuario_por_cpf(self, cpf):
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def encontrar_conta_por_numero(self, numero):
        for conta in self.contas:
            if conta.numero == numero and conta.ativo:
                return conta
        return None

    def login(self):
        cpf = input("Digite seu CPF para login: ")
        usuario = self.encontrar_usuario_por_cpf(cpf)
        if not usuario:
            print("❌ Usuário não encontrado.")
            return

        contas_do_usuario = [c for c in self.contas if c.usuario_cpf == cpf and c.ativo]
        if not contas_do_usuario:
            print("❌ Você não possui conta ativa.")
            return

        print("Selecione sua conta:")
        for conta in contas_do_usuario:
            print(f"Número: {conta.numero} | Agência: {conta.agencia}")

        numero_selecionado = int(input("Digite o número da conta desejada: "))
        conta_selecionada = self.encontrar_conta_por_numero(numero_selecionado)

        if not conta_selecionada or conta_selecionada not in contas_do_usuario:
            print("❌ Conta inválida ou inativa.")
            return

        self.usuario_logado = usuario
        self.conta_ativa = conta_selecionada
        print(f"🔓 Login realizado com sucesso! Bem-vindo(a), {usuario.nome}.")

    def exibir_saldo(self):
        saldo_disponivel = self.saldo + self.LIMITE_CHEQUE_ESPECIAL
        print("💰 Você escolheu a opção Saldo!")
        print(f"💼 Saldo disponível: R$ {self.saldo:.2f}")
        print(f"💳 Limite Cheque Especial: R$ {self.LIMITE_CHEQUE_ESPECIAL:.2f}")
        print(f"🏦 Saldo + Limite: R$ {saldo_disponivel:.2f}")

    def sacar(self):
        agora = datetime.now(pytz.timezone("America/Sao_Paulo"))

        if self.data_ultimo_saque != agora.date():
            self.contagem_saques_hoje = 0
            self.data_ultimo_saque = agora.date()

        if self.contagem_saques_hoje >= self.LIMITE_SAQUES:
            print("⚠️ Você já realizou os 3 saques permitidos hoje.")
            return

        if agora.hour >= 22 or agora.hour < 8:
            limite_saque = (self.saldo + self.LIMITE_CHEQUE_ESPECIAL) / 2
            print("🌙 Saques após as 22h são limitados a 50% do saldo disponível.")
        else:
            limite_saque = min(self.saldo + self.LIMITE_CHEQUE_ESPECIAL, self.VALOR_MAX_SAQUE)

        print(f"💵 Seu limite de saque atual é de R$ {limite_saque:.2f}")
        valor = float(input("Digite o valor do saque: "))

        if valor <= limite_saque:
            self.saldo -= valor
            self.contagem_saques_hoje += 1
            self.historico.adicionar_registro("Saque", valor, "Efetivado", self.conta_ativa.numero)
            self.salvar_dados()
            print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
            print("Retire seu dinheiro na boca do caixa.")
        else:
            print("❌ Valor excede o limite permitido para saque.")
            print("Tente novamente com um valor menor.")

    def depositar(self):
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

        self.historico.adicionar_registro("Depósito", valor, "Pendente", self.conta_ativa.numero)
        print(f"✅ Depósito de R$ {valor:.2f} agendado para {compensacao.strftime('%d/%m/%Y %H:%M')}")
        self.salvar_dados()

    def exibir_extrato(self):
        extrato_filtrado = self.historico.filtrar_por_conta(self.conta_ativa.numero)
        print("📄 Você escolheu a opção Extrato!")
        print("-" * 40)
        if not extrato_filtrado:
            print("🔍 Nenhuma operação registrada.")
        else:
            for op in sorted(extrato_filtrado, key=lambda x: x["data"]):
                data_formatada = datetime.fromisoformat(op["data"]).strftime("%d/%m/%Y %H:%M")
                print(f"{op['tipo']} | R$ {op['valor']:.2f} | {data_formatada} | {op['status']}")
        print("-" * 40)

    def criar_usuario(self):
        print("🧾 Cadastrar novo usuário")
        nome = input("Nome completo: ")
        nascimento = input("Data de nascimento (dd/mm/yyyy): ")
        cpf = input("CPF (somente números): ").strip()
        endereco = input("Endereço (logradouro, número - bairro - cidade/sigla - cep): ")

        if not self.validar_cpf(cpf):
            print("❌ CPF inválido.")
            return

        if self.encontrar_usuario_por_cpf(cpf):
            print("⚠️ Já existe um usuário com esse CPF.")
            return

        self.usuarios.append(Usuario(nome, nascimento, cpf, endereco))
        self.salvar_dados()
        print("✅ Usuário cadastrado com sucesso!")

    def criar_conta_corrente(self):
        cpf = input("Digite o CPF do usuário para vincular a conta: ")
        usuario = self.encontrar_usuario_por_cpf(cpf)
        if not usuario:
            print("❌ Usuário não encontrado.")
            return

        nova_conta = Conta(self.prox_numero_conta, cpf)
        self.contas.append(nova_conta)
        self.prox_numero_conta += 1
        self.salvar_dados()
        print(f"✅ Conta criada com sucesso! Número da conta: {nova_conta.numero}")


# --- LOOP PRINCIPAL DO SISTEMA ---

banco = Banco()
banco.carregar_dados()

while True:
    if not banco.usuario_logado:
        print("\nLOGIN")
        print("1 - Fazer login")
        print("2 - Criar usuário")
        print("3 - Criar conta corrente")
        print("0 - Sair")
        opcao_login = int(input("Escolha uma opção: "))
        if opcao_login == 1:
            banco.login()
        elif opcao_login == 2:
            banco.criar_usuario()
        elif opcao_login == 3:
            banco.criar_conta_corrente()
        elif opcao_login == 0:
            print("👋 Sistema encerrado. Obrigado por usar nosso banco!")
            break
        else:
            print("❌ Opção inválida.")
    else:
        print("\nMENU PRINCIPAL")
        print("1 - Depositar")
        print("2 - Saldo")
        print("3 - Extrato")
        print("4 - Sacar")
        print("0 - Sair")
        opcao_menu = int(input("Escolha uma opção: "))
        if opcao_menu == 1:
            banco.depositar()
        elif opcao_menu == 2:
            banco.exibir_saldo()
        elif opcao_menu == 3:
            banco.exibir_extrato()
        elif opcao_menu == 4:
            banco.sacar()
        elif opcao_menu == 0:
            print(f"👋 Até breve, {banco.usuario_logado.nome}!")
            banco.usuario_logado = None
            banco.conta_ativa = None
        else:
            print("❌ Opção inválida.")