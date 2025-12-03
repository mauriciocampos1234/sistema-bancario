
# 🏦 Banco Digital em Python

Este projeto simula um sistema de **banco digital** com funcionalidades básicas como depósitos (em dinheiro ou cheque), saques, consulta de saldo, extrato e exportação de movimentações.

---

## 🚀 Funcionalidades

- **Depósito com compensação:**
  - 💵 Dinheiro: Compensação no mesmo dia útil até 18h, ou no próximo dia útil após 16h ou fim de semana.
  - 🧾 Cheque: Compensação em até 2 a 3 dias úteis.
- **Saque com regras realistas:**
  - Limite de **3 saques por dia**.
  - Valor máximo de **R$ 500 por saque**.
  - Saques **após as 22h limitados a 50% do saldo disponível**.
- **Saldo atualizado** com separação entre valores disponíveis e pendentes.
- **Extrato completo** com status da operação (Efetivado ou Pendente).
- **Exportação do extrato** em `.txt` ou `.csv`.

---

## 📂 Estrutura do Código

### 1. Controle de Depósitos
- Armazenamento dos depósitos com status `Pendente`.
- Verificação periódica (a cada operação) se o horário de compensação foi alcançado.
- Atualização do saldo e do histórico.

### 2. Controle de Saques
- Contador diário resetado automaticamente ao mudar a data.
- Restrição de horário: saques entre 22h e 08h são limitados a 50% do saldo.
- Limite de valor por saque: R$ 500.

### 3. Extrato Bancário
- Apresenta todas as operações em ordem cronológica.
- Exibe status de **pendente** ou **efetivado**.
- Exportação disponível em:
  - `.txt`: formato legível.
  - `.csv`: compatível com planilhas (Excel, Google Sheets, etc.).

---

## 🛠 Tecnologias utilizadas

- **Python 3.11 ou superior**
- Módulos padrão:
  - `datetime`
  - `csv`

---

# 🏦 Banco Digital em Python (Segunda fase do projeto)

# 🛠️ Funcionalidades Implementadas
O sistema bancário foi desenvolvido em Python com o objetivo de simular operações básicas de uma conta corrente, com persistência de dados via JSON e controle de acesso por usuário e conta. A seguir estão as funcionalidades implementadas com base no código original e nas melhorias realizadas:

## 1. Cadastro de Usuários
Cada usuário é composto por:
Nome completo
Data de nascimento
CPF (somente números)
Endereço (formato: logradouro, número - bairro - cidade/sigla - CEP)
O sistema garante que não haja dois usuários com o mesmo CPF.

## 2. Cadastro de Contas Correntes
Cada conta possui:
Agência fixa (0001)
Número sequencial iniciado em 1
Vínculo com um único usuário
Um usuário pode possuir mais de uma conta.

## 3. Login do Usuário
Autenticação por CPF
Após login bem-sucedido, o usuário seleciona a conta ativa entre as disponíveis
As operações são vinculadas à conta selecionada

## 4. Operações Bancárias
✅ Depósito
Permite escolher entre depósito em dinheiro ou cheque
Registra histórico com status inicial como "Pendente"
Agendamento automático de compensação conforme regras de horário e dia útil

✅ Saque
Limite diário de até 3 saques
Valor máximo por saque: R$ 500,00
Integração com cheque especial (limite adicional de R$ 1000,00 )
Saques noturnos (antes das 8h ou após as 22h) limitados a 50% do saldo disponível + limite

✅ Saldo
Exibe o saldo atual e depósitos pendentes
Mostra também:
O valor do limite concedido pelo banco
O total disponível (saldo + limite)

✅ Extrato
Exibe todas as operações realizadas na conta ativa
Histórico filtrado automaticamente pela conta selecionada
Permite exportar extrato para:
Arquivo .txt
Arquivo .csv

## 5. Persistência de Dados
Todos os dados (usuários, contas e histórico) são salvos em um arquivo JSON chamado dados_bancarios.json
Garantia de persistência entre sessões do programa

### Para uma melhor visualização(Formatação) dos dados que são gerados em JSON
💻 [jsonviewe](https://jsonviewer.stack.hu/)

## 6. Histórico por Conta
Cada operação registrada está vinculada ao número da conta
O extrato mostra apenas as operações da conta ativa

## 7. Modo de Teste
A função compensar_depositos() foi comentada no loop principal para facilitar testes
Isso permite realizar saques mesmo sem aguardar a compensação dos depósitos
Ideal para validar rapidamente o uso do cheque especial e outras operações

# 🏦 Banco Digital em Python (Terceira fase do projeto)

# 🛠️ Funcionalidades Implementadas
Modelar o sistema bancário com Programação Orientada a Objetos (POO) em Python , mantendo todas as funcionalidades do sistema, mas agora com uma arquitetura mais profissional e escalável.


## 🧪 Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/banco-digital-python.git
   ```

2. Navegue até o diretório do projeto:
   ```bash
   cd banco-digital-python
   ```

3. Execute o programa:
   ```bash
   python banco_digital.py
   ```

---

## ✍️ Autor

**Maurício Campos**  
Desenvolvedor Full Stack | Estudante de Desenvolvimento Python | Java | PHP | C# | Front-end | na Universidade Estácio de Sá  
📍 [LinkedIn](https://www.linkedin.com/in/mauricio-campos-4a666b317)  
💻 [GitHub](https://github.com/mauriciocampos1234)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
