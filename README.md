
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
Desenvolvedor Full Stack | Estudante de Desenvolvimento Java na Estácio  
📍 [LinkedIn](https://www.linkedin.com/in/mauricio-campos-4a666b317)  
💻 [GitHub](https://github.com/mauriciocampos1234)

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
