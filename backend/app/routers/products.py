import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, inspect
from app.database import get_db
from app.models.produto import Produto
from app.models.item_pedido import ItemPedido
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.schemas import ProdutoRead, ProdutoUpdate
from typing import List, Optional

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.get("/") # Removemos o response_model temporariamente para facilitar o envio da média
def listar_produtos(
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 20,
    busca: Optional[str] = None
):
    # 1. Criamos uma subquery para calcular a média de cada produto
    subquery_media = db.query(
        ItemPedido.id_produto,
        func.avg(AvaliacaoPedido.avaliacao).label("media")
    ).join(AvaliacaoPedido, ItemPedido.id_pedido == AvaliacaoPedido.id_pedido)\
     .group_by(ItemPedido.id_produto).subquery()

    # 2. Fazemos a query principal unindo o Produto com a média calculada
    query = db.query(Produto, subquery_media.c.media)\
              .outerjoin(subquery_media, Produto.id_produto == subquery_media.c.id_produto)

    if busca:
        query = query.filter(
            or_(
                Produto.nome_produto.ilike(f"%{busca}%"),
                Produto.categoria_produto.ilike(f"%{busca}%")
            )
        )

    results = query.offset(skip).limit(limit).all()

    # 3. Formatamos a saída para o JSON ficar certinho
    lista_final = []
    for produto, media in results:
        p_dict = {c.key: getattr(produto, c.key) for c in inspect(produto).mapper.column_attrs}
        p_dict["media_avaliacao"] = round(media, 2) if media else 0
        lista_final.append(p_dict)
        
    return lista_final

@router.get("/{id_produto}")
def obter_detalhes(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # 1. Média de avaliações (você já tinha)
    media = db.query(func.avg(AvaliacaoPedido.avaliacao))\
        .join(ItemPedido, ItemPedido.id_pedido == AvaliacaoPedido.id_pedido)\
        .filter(ItemPedido.id_produto == id_produto).scalar()
    
    # 2. Contagem de vendas (Total de itens pedidos desse ID)
    vendas = db.query(func.count(ItemPedido.id_item))\
        .filter(ItemPedido.id_produto == id_produto).scalar()
    
    return {
        "produto": produto, 
        "media": round(media, 2) if media else 0,
        "vendas": vendas or 0
    }

# 1. ADICIONAR (POST)
@router.post("/", status_code=201)
def criar_produto(produto: ProdutoUpdate, db: Session = Depends(get_db)):
    try:
        novo_produto = Produto(
            id_produto=str(uuid.uuid4()),
            nome_produto=produto.nome_produto,
            categoria_produto=produto.categoria_produto,
            peso_produto_gramas=produto.peso_produto_gramas, # Verifique esse nome!
            comprimento_centimetros=produto.comprimento_centimetros,
            altura_centimetros=produto.altura_centimetros,
            largura_centimetros=produto.largura_centimetros
        )
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
        return novo_produto
    except Exception as e:
        db.rollback()
        print(f"Erro detalhado: {e}") # Isso vai te ajudar a ver o nome real da coluna
        raise HTTPException(status_code=500, detail=str(e))

# 2. ATUALIZAR (PUT)
@router.put("/{id_produto}")
def atualizar_produto(id_produto: str, dados: ProdutoUpdate, db: Session = Depends(get_db)):
    db_produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    # Atualiza apenas os campos que vieram no JSON
    db_produto.nome_produto = dados.nome_produto
    db_produto.categoria_produto = dados.categoria_produto
    db_produto.peso_produto_gramas = dados.peso_produto_gramas
    db_produto.comprimento_centimetros = dados.comprimento_centimetros
    db_produto.altura_centimetros = dados.altura_centimetros
    db_produto.largura_centimetros = dados.largura_centimetros
    
    db.commit()
    db.refresh(db_produto)
    return db_produto

# 3. REMOVER (DELETE)
@router.delete("/{id_produto}")
def remover_produto(id_produto: str, db: Session = Depends(get_db)):
    db_produto = db.query(Produto).filter(Produto.id_produto == id_produto).first()
    if not db_produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    db.delete(db_produto)
    db.commit()
    return {"message": "Produto removido com sucesso"}