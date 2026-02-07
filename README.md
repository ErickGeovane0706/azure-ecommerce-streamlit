# 📦 Azure Product Manager

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)
![Azure SQL](https://img.shields.io/badge/Azure_SQL-0078D4?style=for-the-badge&logo=microsoft-azure)
![Azure Blob](https://img.shields.io/badge/Azure_Blob_Storage-0089D6?style=for-the-badge&logo=microsoft-azure)

> Um sistema completo de **Gestão de Produtos (CRUD)** desenvolvido em Python, utilizando a nuvem da **Microsoft Azure** para armazenamento de dados relacionais e arquivos de mídia.

---

## 📸 Screenshots

| Tela de Cadastro | Gerenciamento e Listagem |
|:---:|:---:|
| <img src="https://github.com/user-attachments/assets/46bd42c6-a130-483f-892e-e549bd17ea0e" width="100%"> | <img src="https://github.com/user-attachments/assets/b17256fd-ce24-40e8-a39f-1780831554c5" width="100%"> |


---

## 🚀 Funcionalidades

- **☁️ Integração Nuvem Híbrida:**
  - Dados do produto (Nome, Preço, Descrição) salvos no **Azure SQL Database**.
  - Imagens dos produtos enviadas automaticamente para o **Azure Blob Storage**.
- **🛠️ CRUD Completo:**
  - **C**reate: Cadastro com upload de imagem.
  - **R**ead: Listagem visual com cards.
  - **U**pdate: Edição de preço, nome e descrição.
  - **D**elete: Remoção segura do registro.
- **💻 Interface Moderna:** UI limpa e responsiva construída com **Streamlit**.

---

## 📦 Pré-requisitos

Antes de começar, você precisará ter instalado:
- [Python 3.9+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- Uma conta ativa no **Microsoft Azure**.

---

## 🔧 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone https://github.com/ErickGeovane0706/azure-ecommerce-streamlit.git
```
### 2. Crie um ambiente virtual

```Bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```
### 3. Instale as dependências
```Bash
pip install -r requirements.txt
```
### 4. Configure as Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto (use o .env.example como base) e preencha com suas credenciais do Azure:

```Ini, TOML

BLOB_CONNECTION_STRING="sua_string_de_conexao_do_storage"
BLOB_CONTAINER_NAME="seu_container"
BLOB_ACCOUNT_NAME="seu_nome_da_conta_storage"

SQL_SERVER="seu_servidor.database.windows.net"
SQL_DATABASE="seu_banco_de_dados"
SQL_USER="seu_usuario"
SQL_PASSWORD="sua_senha"
```
## ▶️ Como Rodar
Com tudo configurado, execute o comando:

```Bash
streamlit run main.py
O navegador abrirá automaticamente no endereço http://localhost:8501.
```
## 🛡️ Segurança
Este projeto utiliza variáveis de ambiente (.env) para proteger credenciais sensíveis. Nunca suba o arquivo .env para o GitHub.
