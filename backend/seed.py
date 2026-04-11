import pandas as pd
import numpy as np
from app.database import SessionLocal
from app.models.consumidor import Consumidor
from app.models.vendedor import Vendedor
from app.models.produto import Produto
from app.models.pedido import Pedido
from app.models.item_pedido import ItemPedido
from app.models.avaliacao_pedido import AvaliacaoPedido

def seed_database():
    db = SessionLocal()
    try:
        print("🚀 Iniciando a carga de dados com tratamento de nulos...")

        # 1. Consumidores
        print("📥 Populando Consumidores...")
        df_cons = pd.read_csv("data/dim_consumidores.csv").drop_duplicates(subset=['id_consumidor'])
        # Garante que nome e cep não sejam nulos
        df_cons['nome_consumidor'] = df_cons['nome_consumidor'].fillna('Consumidor Padrão')
        df_cons['prefixo_cep'] = df_cons['prefixo_cep'].fillna(0)
        
        for _, row in df_cons.iterrows():
            db.add(Consumidor(
                id_consumidor=row['id_consumidor'],
                prefixo_cep=row['prefixo_cep'],
                nome_consumidor=row['nome_consumidor'],
                cidade=row['cidade'],
                estado=row['estado']
            ))

        # 2. Vendedores
        print("📥 Populando Vendedores...")
        df_vend = pd.read_csv("data/dim_vendedores.csv").drop_duplicates(subset=['id_vendedor'])
        df_vend['nome_vendedor'] = df_vend['nome_vendedor'].fillna('Vendedor Padrão')
        
        for _, row in df_vend.iterrows():
            db.add(Vendedor(
                id_vendedor=row['id_vendedor'],
                nome_vendedor=row['nome_vendedor'],
                prefixo_cep=row['prefixo_cep'],
                cidade=row['cidade'],
                estado=row['estado']
            ))

        # 3. Produtos (Resolvendo o erro da categoria)
        print("📥 Populando Produtos...")
        df_prod = pd.read_csv("data/dim_produtos.csv").drop_duplicates(subset=['id_produto'])
        # AQUI ESTÁ A SOLUÇÃO: Substitui categorias vazias por 'sem_categoria'
        df_prod['categoria_produto'] = df_prod['categoria_produto'].fillna('sem_categoria')
        df_prod['nome_produto'] = df_prod['nome_produto'].fillna('Produto sem nome')
        
        for _, row in df_prod.iterrows():
            db.add(Produto(
                id_produto=row['id_produto'],
                nome_produto=row['nome_produto'],
                categoria_produto=row['categoria_produto'],
                peso_produto_gramas=row['peso_produto_gramas'] if pd.notnull(row['peso_produto_gramas']) else 0,
                comprimento_centimetros=row['comprimento_centimetros'] if pd.notnull(row['comprimento_centimetros']) else 0,
                altura_centimetros=row['altura_centimetros'] if pd.notnull(row['altura_centimetros']) else 0,
                largura_centimetros=row['largura_centimetros'] if pd.notnull(row['largura_centimetros']) else 0
            ))

        # 4. Pedidos
        print("📥 Populando Pedidos...")
        df_ped = pd.read_csv("data/fat_pedidos.csv").drop_duplicates(subset=['id_pedido'])
        for _, row in df_ped.iterrows():
            db.add(Pedido(id_pedido=row['id_pedido'], id_consumidor=row['id_consumidor'], status=row['status']))

        # 5. Itens
        print("📥 Populando Itens...")
        df_itens = pd.read_csv("data/fat_itens_pedidos.csv")
        for _, row in df_itens.iterrows():
            db.add(ItemPedido(
                id_pedido=row['id_pedido'],
                id_item=row['id_item'],
                id_produto=row['id_produto'],
                id_vendedor=row['id_vendedor'],
                preco_BRL=row['preco_BRL'],
                preco_frete=row['preco_frete']
            ))

        # 6. Avaliações
        print("📥 Populando Avaliações...")
        df_aval = pd.read_csv("data/fat_avaliacoes_pedidos.csv").drop_duplicates(subset=['id_avaliacao'])
        for _, row in df_aval.iterrows():
            db.add(AvaliacaoPedido(
                id_avaliacao=row['id_avaliacao'],
                id_pedido=row['id_pedido'],
                avaliacao=row['avaliacao']
            ))

        print("💾 Salvando alterações no banco...")
        db.commit()
        print("✅ SUCESSO! O banco foi populado e os dados nulos foram tratados.")

    except Exception as e:
        print(f"❌ Erro durante o seed: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()