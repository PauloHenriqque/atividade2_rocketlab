from pydantic import BaseModel
from typing import Optional

class ProdutoBase(BaseModel):
    nome_produto: str
    categoria_produto: str
    peso_produto_gramas: Optional[float] = None
    comprimento_centimetros: Optional[float] = None
    altura_centimetros: Optional[float] = None
    largura_centimetros: Optional[float] = None

class ProdutoUpdate(BaseModel):
    nome_produto: Optional[str] = None
    peso_produto_gramas: Optional[float] = None

class ProdutoRead(ProdutoBase):
    id_produto: str
    class Config:
        from_attributes = True