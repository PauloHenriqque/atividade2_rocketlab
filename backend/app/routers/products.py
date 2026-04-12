from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.produto import Produto
from app.models.item_pedido import ItemPedido
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.schemas import ProdutoRead, ProdutoUpdate

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/", response_model=list[ProdutoRead])
def listar_produtos(db: Session = Depends(get_db), skip: int = 0, limit: int = 20):
    return db.query(Produto).offset(skip).limit(limit).all()

@router.get("/{id_produto}")
def obter_detalhes(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    media = db.query(func.avg(AvaliacaoPedido.avaliacao))\
        .join(ItemPedido, ItemPedido.id_pedido == AvaliacaoPedido.id_pedido)\
        .filter(ItemPedido.id_produto == id_produto).scalar()
    
    return {"produto": produto, "media": round(media, 2) if media else 0}