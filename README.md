# 🚛 ERP de Logística Full-Stack

Sistema corporativo de gestão logística desenvolvido do zero, integrando um banco de dados relacional robusto, uma API moderna e de Alta performance, e um painel interativo visual.

## 🚀 Tecnologias Utilizadas

O projeto foi construído utilizando uma arquitetura moderna separada em camadas:
- **Banco de Dados:** PostgreSQL (rodando de forma isolada via Docker)
- **Backend (API):** Python com FastAPI e Pydantic (validação de dados)
- **Frontend (Painel Visual):** Streamlit
- **Gerenciamento de Dependências e Segurança:** `python-dotenv` para variáveis de ambiente e `psycopg2` para conexão SQL.

---

## 📂 Estrutura do Projeto

```text
ERP/
│
├── main.py            # Backend da API (FastAPI + Conexão SQL)
├── painel.py          # Frontend interativo (Streamlit)
├── .env               # Variáveis de ambiente e credenciais (Segredo local)
├── .gitignore         # Arquivos ignorados pelo Git
└── README.md          # Documentação do projeto


⚙️ Como Executar o Projeto Localmente
Siga os passos abaixo para rodar o sistema na sua máquina:

1. Pré-requisitos
Certifique-se de ter instalado no seu computador:

Python (versão 3.10 ou superior)

Docker (com o container do PostgreSQL rodando)

2. Configurar o Ambiente Virtual
Abra o terminal na pasta do projeto e ative o ambiente virtual:

Bash
# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
3. Instalar as Dependências
Com o ambiente virtual ativo, instale as bibliotecas necessárias:

Bash
pip install fastapi uvicorn streamlit requests psycopg2-binary python-dotenv
4. Configurar as Variáveis de Ambiente
Crie um arquivo chamado .env na raiz do projeto e configure as credenciais do seu banco de dados PostgreSQL:

Snippet de código
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=erp_logistica
5. Executar o Sistema (Dois Terminais)
Para o sistema funcionar completo, você precisará de dois terminais abertos simultaneamente:

Terminal 1 (Ligar o Motor / Backend):

Bash
uvicorn main:app --reload
Terminal 2 (Ligar a Tela / Frontend):

Bash
streamlit run painel.py
O painel visual abrirá automaticamente no seu navegador padrão (http://localhost:8501).

💡 Funcionalidades do Sistema
Motoristas: Cadastro completo, listagem em tempo real e remoção segura (com validação de integridade do banco).

Veículos: Gestão de frota com controle de placa, modelo e capacidade em quilogramas.

Viagens: Relacionamento relacional (Chave Estrangeira) unindo motoristas e veículos para o despacho de cargas.

Desenvolvido com dedicação por Bruno Lopes
