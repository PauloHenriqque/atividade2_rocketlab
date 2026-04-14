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
    nome_produto: str
    categoria_produto: str
    comprimento_centimetros: Optional[float] = 10.0
    altura_centimetros: Optional[float] = 10.0
    largura_centimetros: Optional[float] = 10.0  # Adicione largura se não tiver
    peso_produto_gramas: Optional[float] = 100.0 # Nome exato do seu banco

class ProdutoRead(ProdutoBase):
    id_produto: str
    class Config:
        from_attributes = True