import os
from fastapi import FastAPI
from dotenv import load_dotenv

# 1. Carrega as variáveis secretas do arquivo .env
load_dotenv()

# 2. Pega os dados com segurança
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

app = FastAPI()

# Função de conexão usando as variáveis seguras
def get_db_connection():
    import psycopg2
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

# Restante das suas rotas e códigos do FastAPI...


from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

#Ligação a nossa API
app = FastAPI(title="API - ERP Logistica")

# Credenciais de conexão com o banco de dados
DB_CONFIG = {
    "dbname": "erp_logistica",
    "user": "admin",
    "password": "adminpassword",
    "host": "localhost",
    "port": "5433"
}

# Função para criar a conexão com o banco de dados
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


class MotoristaBase(BaseModel):
    nome: str
    cnh: str
    categoria_cnh: str

class VeiculoBase(BaseModel):
    placa: str
    modelo: str
    capacidade_kg: float 

class ViagemBase(BaseModel):
    motorista_id: int
    veiculo_id: int
    origem: str
    destino: str
    

# ---------------------------------------------------
# Nossas Rotas (Endpoints)
# ---------------------------------------------------

@app.get("/")
def rota_principal():
    return {"mensagem": "A API do ERP Logistica está funcionando!"}

@app.get("/motoristas")
def listar_motoristas():
    try:
        # 1 passo - Abrir a conexão com o banco de dados
        conn = get_db_connection()
        # 2 passo - Criar um cursor para executar a consulta no formato JSON (Dicionario)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        # 3 passo - Executar a consulta SQL para listar os motoristas
        cursor.execute("SELECT * FROM Motoristas;")
        # 4 passo - Obter os resultados da consulta
        motoristas = cursor.fetchall()

        # 5 passo - Fechar o cursor e a conexão com o banco de dados
        cursor.close()
        conn.close()

        return motoristas
    except Exception as e:
        return {"erro_banco": str(e)}



# ----------------------------------------------------
# 1. Nova Rota para cadastrar um novo motorista
# ----------------------------------------------------

@app.post("/motoristas")
def cadastrar_motorista(motorista: MotoristaBase):
    try:
        # 1 passo - Abrir a conexão com o banco de dados
        conn = get_db_connection()
        cursor = conn.cursor()

        # O sql de inserção de dados no banco de dados
        sql = "INSERT INTO Motoristas (nome, cnh, categoria_cnh) VALUES (%s, %s, %s) RETURNING id;"
        valores = (motorista.nome, motorista.cnh, motorista.categoria_cnh)

        cursor.execute(sql, valores)
        novo_id = cursor.fetchone()[0]  # Obter o ID do novo motorista inserido

        # confirmar a transação
        conn.commit()

        cursor.close()
        conn.close()

        return {"mensagem": "Motorista cadastrado com sucesso!", "id": novo_id}
    except Exception as e:
        return {"erro_banco": str(e)}

@app.put("/motoristas/{motorista_id}")
def atualizar_motorista(motorista_id: int, motorista: MotoristaBase):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "UPDATE Motoristas SET nome = %s, cnh = %s, categoria_cnh = %s WHERE id = %s;"
        valores = (motorista.nome, motorista.cnh, motorista.categoria_cnh, motorista_id)

        cursor.execute(sql, valores)
        id_atualizado = cursor.rowcount  # Obter o número de linhas afetadas pela atualização
        conn.commit()

        cursor.close()
        conn.close()

        if id_atualizado:
            return {"mensagem": "Motorista atualizado com sucesso!"}
        else:
            return {"mensagem": "Motorista não encontrado."}
    except Exception as e:
        return {"erro_banco": str(e)}

@app.delete("/motoristas/{motorista_id}")
def deletar_motorista(motorista_id: int):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM Motoristas WHERE id = %s RETURNING id;"
        cursor.execute(sql, (motorista_id,))
        id_deletado = cursor.fetchone()  # Obter o ID do motorista deletado
        conn.commit()

        cursor.close()
        conn.close()

        if id_deletado:
            return {"mensagem": "Motorista deletado com sucesso!"}
        else:
            return {"mensagem": "Motorista não encontrado."}
    except Exception as e:
        return {"erro_banco": str(e)}


@app.get("/veiculos")
def listar_veiculos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Veiculos;")
        veiculos = cursor.fetchall()
        cursor.close()
        conn.close()
        return veiculos
    except Exception as e:
        return {"erro_banco": str(e)}

@app.post("/veiculos")
def cadastrar_veiculo(veiculo: VeiculoBase):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO Veiculos (placa, modelo, capacidade_kg) VALUES (%s, %s, %s) RETURNING id;"
        valores = (veiculo.placa, veiculo.modelo, veiculo.capacidade_kg)

        cursor.execute(sql, valores)
        novo_id = cursor.fetchone()[0]
        conn.commit()

        cursor.close()
        conn.close()

        return {"mensagem": "Veículo cadastrado com sucesso!", "id": novo_id}
    except Exception as e:
        return {"erro_banco": str(e)}


    #----------------------------------------------------
    # 1. Nova Rota para cadastrar uma nova viagem
    #----------------------------------------------------

@app.get("/viagens")
def listar_viagens():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM Viagens_Cargas;")
        viagens = cursor.fetchall()
        cursor.close()
        conn.close()
        return viagens
    except Exception as e:
        return {"erro_banco": str(e)}

@app.post("/viagens")
def criar_viagem(viagem: ViagemBase):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO Viagens_Cargas (motorista_id, veiculo_id, origem, destino) VALUES (%s, %s, %s, %s) RETURNING id;"
        valores = (viagem.motorista_id, viagem.veiculo_id, viagem.origem, viagem.destino)
        cursor.execute(sql, valores)
        novo_id = cursor.fetchone()[0] 
        conn.commit() 
        cursor.close()
        conn.close()
        return {"mensagem": "Viagem criada com sucesso!", "id_novo": novo_id}
    except Exception as e:
        return {"erro_banco": str(e)}

        


