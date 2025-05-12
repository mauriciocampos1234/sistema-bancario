from datetime import datetime, timedelta
import pytz #Poderiamos usar o timedelta do python, mas o pytz é menos verboso, mais declarativo e mais fácil de usar
import csv

# Saldo inicial zerado
saldo = 0.0
opcao = -1

# Limites
LIMITE_DEPOSITOS = 3
LIMITE_EXTRATOS = 3
LIMITE_SAQUES_DIA = 3
VALOR_MAX_SAQUE = 500

# Contadores
contagem_depositos = 0
contagem_extratos = 0
contagem_saques_hoje = 0
data_ultimo_saque = datetime.now(pytz.timezone("America/Sao_Paulo")).date()

# Armazenamento
depositos_pendentes = []
historico = []

# Função de compensação de depósitos
def compensar_depositos():
    global saldo
    agora = datetime.now(pytz.timezone("America/Sao_Paulo")) # Responsável por pegar a data e hora atual, verifica se o depósito já pode ser compensado
    for deposito in depositos_pendentes[:]:  # cópia da lista
        if agora >= deposito["compensacao"]:
            saldo += deposito["valor"]
            deposito["status"] = "Efetivado"
            historico.append({ #Dicionário e append para o histórico, parece Json mas é o padrão python para facilitar a leitura e manipulação
                "tipo": "Depósito",
                "valor": deposito["valor"],
                "data": agora,
                "status": "Efetivado"
            })
            depositos_pendentes.remove(deposito)
            print(f"Depósito compensado: R$ {deposito['valor']:.2f}")

# Loop principal
while opcao != 0:
    compensar_depositos()

    opcao = int(input(
        "\nInforme a opção desejada: \n"
        "1 - Depositar\n"
        "2 - Saldo\n"
        "3 - Extrato\n"
        "4 - Sacar\n"
        "0 - Sair\n"
    ))

    if opcao == 1:
        if contagem_depositos >= LIMITE_DEPOSITOS:
            print("⚠️ Limite máximo de depósitos excedido.")
            continue

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
            # Depósito em dinheiro
            if agora.weekday() >= 5 or hora >= 16:
                compensacao = (agora + timedelta(days=(7 - agora.weekday()) % 7 or 1)).replace(hour=11, minute=0, second=0)
            else:
                compensacao = agora.replace(hour=18, minute=0, second=0)
            print("🟢 Depósito em dinheiro agendado para compensação.")

        elif tipo_opcao == "2":
            # Depósito em cheque
            dias_compensacao = 2
            if agora.weekday() >= 5 or hora >= 16:
                dias_compensacao += 1
            compensacao = agora + timedelta(days=dias_compensacao)
            compensacao = compensacao.replace(hour=18, minute=0, second=0)
            print("🟡 Depósito em cheque agendado para compensação (até 3 dias úteis).")
        else:
            print("❌ Opção inválida. Tente novamente.")
            continue

        depositos_pendentes.append({
            "valor": valor,
            "compensacao": compensacao,
            "status": "Pendente"
        })

        historico.append({
            "tipo": "Depósito",
            "valor": valor,
            "data": agora,
            "status": "Pendente",
            "compensacao": compensacao
        })

        contagem_depositos += 1
        print(f"✅ Depósito de R$ {valor:.2f} agendado para {compensacao.strftime('%d/%m/%Y %H:%M')}") #strftime formata a data e hora, o %d é o dia, 
        #%m é o mês e %Y é o ano, %H é a hora e %M é os minutos (Mascara)
    
    elif opcao == 2:
        print("💰 Você escolheu a opção Saldo!")
        saldo_pendente = sum(d["valor"] for d in depositos_pendentes)
        print(f"💼 Saldo disponível: R$ {saldo:.2f}")
        print(f"🕒 Depósitos pendentes: R$ {saldo_pendente:.2f}")

    elif opcao == 3:
        if contagem_extratos >= LIMITE_EXTRATOS:
            print("⚠️ Limite de extratos excedido.")
            continue

        print("📄 Você escolheu a opção Extrato!")
        print("-" * 40) #exibir uma linha composta por 40 caracteres de hífen (-), No caso, a expressão "-" * 40 resulta em 
        #uma string que contém exatamente 40 hífens consecutivos, como "----------------------------------------".
        if not historico:
            print("🔍 Nenhuma operação registrada.")
        else:
            for op in sorted(historico, key=lambda x: x["data"]): #função sorted ordenando o iterável e Colocando em ordem crescente
                data_formatada = op["data"].strftime("%d/%m/%Y %H:%M")
                print(f"{op['tipo']} | R$ {op['valor']:.2f} | {data_formatada} | {op['status']}")
                if op["status"] == "Pendente":
                    print(f"  → Compensação prevista: {op['compensacao'].strftime('%d/%m/%Y %H:%M')}")

        print("-" * 40)
        contagem_extratos += 1

        exportar = input("Deseja exportar o extrato? (s/n): ").lower()
        if exportar == "s":
            formato = input("Escolha o formato: 1 - TXT | 2 - CSV: ")
            if formato == "1":
                with open("extrato_bancario.txt", "w", encoding="utf-8") as f:
                    f.write("=== Extrato Bancário ===\n")
                    for op in historico:
                        data_formatada = op["data"].strftime("%d/%m/%Y %H:%M")
                        f.write(f"{op['tipo']} | R$ {op['valor']:.2f} | {data_formatada} | {op['status']}\n")
                        if op["status"] == "Pendente":
                            f.write(f"  → Compensação: {op['compensacao'].strftime('%d/%m/%Y %H:%M')}\n")
                print("📁 Extrato exportado para 'extrato_bancario.txt'.")

            elif formato == "2":
                with open("extrato_bancario.csv", "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Tipo", "Valor", "Data", "Status", "Compensação"])
                    for op in historico:
                        compensacao = op.get("compensacao", "").strftime("%d/%m/%Y %H:%M") if op.get("compensacao") else ""
                        writer.writerow([
                            op["tipo"],
                            f"{op['valor']:.2f}",
                            op["data"].strftime("%d/%m/%Y %H:%M"),
                            op["status"],
                            compensacao
                        ])
                print("📁 Extrato exportado para 'extrato_bancario.csv'.")

    elif opcao == 4:
        print("🏧 Você escolheu a opção Sacar!")
        agora = datetime.now(pytz.timezone("America/Sao_Paulo"))

        # Zera contador de saques se for um novo dia
        if data_ultimo_saque != agora.date():
            contagem_saques_hoje = 0
            data_ultimo_saque = agora.date()

        if contagem_saques_hoje >= LIMITE_SAQUES_DIA:
            print("⚠️ Você já realizou os 3 saques permitidos hoje.")
            continue

        if agora.hour >= 22 or agora.hour < 8:
            limite_saque = saldo / 2
            print("🌙 Saques após as 22h são limitados a 50% do saldo.")
        else:
            limite_saque = min(saldo, VALOR_MAX_SAQUE)

        print(f"💵 Seu limite de saque atual é de R$ {limite_saque:.2f}")
        valor = float(input("Digite o valor do saque: "))

        if valor <= limite_saque:
            saldo -= valor
            contagem_saques_hoje += 1
            historico.append({
                "tipo": "Saque",
                "valor": valor,
                "data": agora,
                "status": "Efetivado"
            })
            print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
            print("Retire seu dinheiro na boca do caixa.")
        else:
            print("❌ Valor excede o limite permitido para saque.")
            print("Tente novamente com um valor menor.")

    elif opcao == 0:
        print("👋 Você escolheu a opção Sair!")
        print("Sistema encerrado com sucesso!")
        print("Obrigado por utilizar nossos serviços, até breve!")
        break