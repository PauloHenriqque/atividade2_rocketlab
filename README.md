🛠️ Como Executar o Projeto

1. Pré-requisitos

Python instalado.
Node.js e npm instalados.

2. Configurando o Backend

Acesse a pasta do backend no seu Terminal:
cd backend

Crie um ambiente virtual:
python -m venv venv

Ative o ambiente virtual:
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

Instale as dependências:
pip install -r requirements.txt

Inicie o servidor:
uvicorn app.main:app --reload

O backend estará rodando em: http://127.0.0.1:8000

3. Configurando o Frontend

Acesse a pasta do frontend:
cd frontend

Instale as dependências:
npm install

Inicie a aplicação:
npm run dev
O frontend estará rodando em: http://localhost:5173
