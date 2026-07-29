import streamlit as st
import requests

# Configuração básica
st.set_page_config(page_title="ERP Logística", page_icon="🚛", layout="wide")
st.title("🚛 Painel do ERP - Logística")
st.write("Navegue pelas abas abaixo para gerenciar o sistema.")
st.divider()

# Criando as Abas de Navegação
aba_motoristas, aba_veiculos, aba_viagens = st.tabs(["👷 Motoristas", "🚚 Veículos", "🗺️ Viagens"])

# ==========================================
# ABA 1: MOTORISTAS (Com Cadastro, Listagem, Edição e Exclusão)
# ==========================================
with aba_motoristas:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cadastrar Novo Motorista")
        with st.form("form_motorista"):
            nome = st.text_input("Nome Completo")
            cnh = st.text_input("Número da CNH")
            categoria = st.selectbox("Categoria", ["A", "B", "C", "D", "E", "AE"])
            
            if st.form_submit_button("Salvar Motorista"):
                dados = {"nome": nome, "cnh": cnh, "categoria_cnh": categoria}
                res = requests.post("http://localhost:8000/motoristas", json=dados)
                if res.status_code == 200:
                    st.success("✅ Salvo com sucesso!")
                else:
                    st.error("❌ Erro ao salvar.")

        st.divider()
        st.subheader("Gerenciar / Excluir Motorista")
        # Buscamos a lista atual para preencher o seletor de exclusão
        res_lista = requests.get("http://localhost:8000/motoristas")
        if res_lista.status_code == 200 and len(res_lista.json()) > 0:
            motoristas = res_lista.json()
            # Criamos um dicionário para mapear "Nome (ID: X)" para o ID real
            opcoes_motoristas = {f"{m['nome']} (ID: {m['id']})": m['id'] for m in motoristas}
            
            escolha = st.selectbox("Selecione o motorista para deletar:", list(opcoes_motoristas.keys()))
            
            if st.button("🗑️ Deletar Motorista Selecionado", type="primary"):
                id_para_deletar = opcoes_motoristas[escolha]
                res_del = requests.delete(f"http://localhost:8000/motoristas/{id_para_deletar}")
                
                if res_del.status_code == 200:
                    resposta_json = res_del.json()
                    if "mensagem" in resposta_json:
                        st.success("✅ Motorista deletado com sucesso!")
                    else:
                        st.error(f"❌ Não foi possível deletar: {resposta_json.get('erro_banco', 'Erro desconhecido')}")
                else:
                    st.error("❌ Erro de comunicação com a API.")
        else:
            st.info("Nenhum motorista cadastrado para gerenciar.")

    with col2:
        st.subheader("Lista de Motoristas")
        if st.button("🔄 Atualizar Motoristas"):
            res = requests.get("http://localhost:8000/motoristas")
            if res.status_code == 200 and len(res.json()) > 0:
                st.dataframe(res.json(), use_container_width=True)
            else:
                st.info("Nenhum registro encontrado.")

# ==========================================
# ABA 2: VEÍCULOS
# ==========================================
with aba_veiculos:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cadastrar Veículo")
        with st.form("form_veiculo"):
            placa = st.text_input("Placa (ex: ABC-1234)")
            modelo = st.text_input("Modelo (ex: Scania R450)")
            capacidade = st.number_input("Capacidade (KG)", min_value=0.0, step=100.0)
            
            if st.form_submit_button("Salvar Veículo"):
                dados = {"placa": placa, "modelo": modelo, "capacidade_kg": capacidade}
                res = requests.post("http://localhost:8000/veiculos", json=dados)
                if res.status_code == 200:
                    st.success("✅ Salvo com sucesso!")
                else:
                    st.error("❌ Erro ao salvar.")

    with col2:
        st.subheader("Lista de Veículos")
        if st.button("🔄 Atualizar Veículos"):
            res = requests.get("http://localhost:8000/veiculos")
            if res.status_code == 200 and len(res.json()) > 0:
                st.dataframe(res.json(), use_container_width=True)
            else:
                st.info("Nenhum registro encontrado.")

# ==========================================
# ABA 3: VIAGENS
# ==========================================
with aba_viagens:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Cadastrar Viagem")
        with st.form("form_viagem"):
            st.write("Digite os IDs correspondentes:")
            motorista_id = st.number_input("ID do Motorista", min_value=1, step=1)
            veiculo_id = st.number_input("ID do Veículo", min_value=1, step=1)
            origem = st.text_input("Cidade de Origem")
            destino = st.text_input("Cidade de Destino")
            
            if st.form_submit_button("Criar Viagem"):
                dados = {
                    "motorista_id": int(motorista_id),
                    "veiculo_id": int(veiculo_id),
                    "origem": origem,
                    "destino": destino
                }
                res = requests.post("http://localhost:8000/viagens", json=dados)
                if res.status_code == 200:
                    st.success("✅ Viagem criada com sucesso!")
                else:
                    st.error("❌ Erro ao salvar. Verifique se os IDs existem.")

    with col2:
        st.subheader("Lista de Viagens")
        if st.button("🔄 Atualizar Viagens"):
            res = requests.get("http://localhost:8000/viagens")
            if res.status_code == 200 and len(res.json()) > 0:
                st.dataframe(res.json(), use_container_width=True)
            else:
                st.info("Nenhum registro encontrado.")