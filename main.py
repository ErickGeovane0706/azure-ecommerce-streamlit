import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import pymssql
import uuid
from dotenv import load_dotenv
from time import sleep # Para dar um tempinho nas mensagens de sucesso

load_dotenv()

# --- Configurações ---
blob_connection_string = os.getenv("BLOB_CONNECTION_STRING")
blob_container_name = os.getenv("BLOB_CONTAINER_NAME")
blob_account_name = os.getenv("BLOB_ACCOUNT_NAME")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

st.set_page_config(page_title="Gestão de Produtos", layout="wide")
st.title("Sistema de Gestão de Produtos (CRUD)")

# --- Funções de Banco de Dados e Storage ---

def get_connection():
    """Função auxiliar para conectar ao banco"""
    return pymssql.connect(server=SQL_SERVER, user=SQL_USER, password=SQL_PASSWORD, database=SQL_DATABASE)

def upload_blob(file):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(blob_connection_string)
        filename = str(uuid.uuid4()) + "_" + file.name
        blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob=filename)
        blob_client.upload_blob(file.read(), overwrite=True)
        return f"https://{blob_account_name}.blob.core.windows.net/{blob_container_name}/{filename}"
    except Exception as e:
        st.error(f"Erro no Upload: {e}")
        return None

# C (CREATE)
def insert_product(name, price, desc, img_url):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = f"INSERT INTO dbo.Produtos (nome, preco, descricao, imagem_url) VALUES ('{name}', {price}, '{desc}', '{img_url}')"
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f'Erro ao salvar: {e}')
        return False

# R (READ)
def list_products():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM dbo.Produtos")
        data = cursor.fetchall()
        conn.close()
        return data
    except Exception as e:
        st.error(f'Erro ao listar: {e}')
        return []

# U (UPDATE)
def update_product(id_produto, name, price, desc):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        # Atualiza apenas os dados de texto/numero, mantendo a imagem antiga
        query = f"UPDATE dbo.Produtos SET nome='{name}', preco={price}, descricao='{desc}' WHERE id={id_produto}"
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f'Erro ao atualizar: {e}')
        return False

# D (DELETE)
def delete_product(id_produto):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = f"DELETE FROM dbo.Produtos WHERE id={id_produto}"
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f'Erro ao excluir: {e}')
        return False

# --- Interface Gráfica (Abas) ---

tab1, tab2 = st.tabs(["🆕 Cadastrar Novo", "📋 Gerenciar Produtos"])

# --- ABA 1: CADASTRO (CREATE) ---
with tab1:
    st.header("Novo Produto")
    with st.form("form_cadastro", clear_on_submit=True):
        name_in = st.text_input("Nome do Produto")
        price_in = st.number_input("Valor (R$)", min_value=0.0, format="%.2f", step=0.01)
        desc_in = st.text_area("Descrição")
        img_in = st.file_uploader("Imagem do Produto", type=["jpg", "png", "jpeg"])

        submitted = st.form_submit_button("Salvar Produto")

        if submitted:
            if name_in and img_in:
                with st.spinner('Enviando para Azure...'):
                    url = upload_blob(img_in)
                    if url and insert_product(name_in, price_in, desc_in, url):
                        st.success("Produto cadastrado com sucesso!")
                        sleep(1)
                        st.rerun() # Recarrega para limpar
            else:
                st.warning("Preencha o nome e envie uma imagem.")

# --- ABA 2: LISTAGEM E EDIÇÃO (READ, UPDATE, DELETE) ---
with tab2:
    st.header("Lista de Produtos")

    # Botão de atualizar lista manual
    if st.button("🔄 Atualizar Lista"):
        st.rerun()

    produtos = list_products()

    if not produtos:
        st.info("Nenhum produto encontrado.")
    else:
        # Loop para exibir cada produto
        for prod in produtos:
            # Estrutura da tupla: (0=id, 1=nome, 2=descricao, 3=preco, 4=imagem_url)
            prod_id = prod[0]
            prod_nome = prod[1]
            prod_desc = prod[2]
            prod_preco = prod[3]
            prod_img = prod[4]

            # Cria um cartão visual para cada produto
            with st.container(border=True):
                col_img, col_dados, col_actions = st.columns([1, 3, 1])

                with col_img:
                    if prod_img:
                        st.image(prod_img, use_container_width=True)

                with col_dados:
                    st.subheader(f"{prod_nome}")
                    st.write(f"**Preço:** R$ {prod_preco}")
                    st.write(f"**Descrição:** {prod_desc}")

                with col_actions:
                    st.write("Ações:")

                    # Botão EXCLUIR (DELETE)
                    # Usamos uma chave única (key) baseada no ID para não confundir os botões
                    if st.button("🗑️ Excluir", key=f"del_{prod_id}"):
                        if delete_product(prod_id):
                            st.success("Excluído!")
                            sleep(1)
                            st.rerun()

                # Área de EDIÇÃO (UPDATE) dentro de um menu expansível
                with st.expander(f"✏️ Editar {prod_nome}"):
                    with st.form(key=f"form_edit_{prod_id}"):
                        new_name = st.text_input("Novo Nome", value=prod_nome)
                        new_price = st.number_input("Novo Preço", value=float(prod_preco), format="%.2f")
                        new_desc = st.text_area("Nova Descrição", value=prod_desc)

                        btn_update = st.form_submit_button("Salvar Alterações")

                        if btn_update:
                            if update_product(prod_id, new_name, new_price, new_desc):
                                st.success("Atualizado com sucesso!")
                                sleep(1)
                                st.rerun()