from fastapi import FastAPI
from app.routers import products
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Sistema de Compras Online")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)

@app.get("/")
def home():
    return {"message": "API Online"}