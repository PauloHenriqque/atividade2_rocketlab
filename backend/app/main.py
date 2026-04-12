from fastapi import FastAPI
from app.routers import products # Você precisará criar um __init__.py na pasta routers

app = FastAPI(title="Sistema de Compras Online")

# Aqui você "anexa" as rotas de produtos
app.include_router(products.router)

@app.get("/")
def home():
    return {"message": "API Online"}