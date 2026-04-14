import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [produtos, setProdutos] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [busca, setBusca] = useState('')
  const [pagina, setPagina] = useState(0)
  const [detalhesProduto, setDetalhesProduto] = useState(null)
  const ITENS_POR_PAGINA = 20

  const fetchProdutos = async (termo = '', novaPagina = 0) => {
    try {
      setCarregando(true);
      const skip = novaPagina * ITENS_POR_PAGINA;
      const url = `http://127.0.0.1:8000/produtos/?busca=${termo}&skip=${skip}&limit=${ITENS_POR_PAGINA}`;
      const response = await fetch(url);
      const data = await response.json();

      if (novaPagina === 0) setProdutos(data);
      else setProdutos(prev => [...prev, ...data]);
      
      setCarregando(false);
    } catch (error) {
      console.error("Erro:", error);
      setCarregando(false);
    }
  };

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      setPagina(0);
      fetchProdutos(busca, 0);
    }, 500);
    return () => clearTimeout(delayDebounceFn);
  }, [busca]);

  const abrirDetalhes = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/produtos/${id}`);
      const data = await response.json();
      setDetalhesProduto(data);
    } catch (error) {
      alert("Erro ao carregar detalhes.");
    }
  };

  // REMOVER PRODUTO
const removerProduto = async (id) => {
  if (window.confirm("Tem certeza que deseja remover este produto?")) {
    try {
      await fetch(`http://127.0.0.1:8000/produtos/${id}`, { method: 'DELETE' });
      // Atualiza a lista removendo o item deletado
      setProdutos(produtos.filter(p => p.id_produto !== id));
      alert("Produto removido!");
    } catch (error) {
      alert("Erro ao remover produto.");
    }
  }
};

// ADICIONAR PRODUTO
const adicionarProduto = async () => {
  const nome = prompt("Nome do produto:");
  const categoria = prompt("Categoria:");

  if (!nome || !categoria) return;

  const novo = {
    nome_produto: nome,
    categoria_produto: categoria,
    comprimento_centimetros: 10,
    altura_centimetros: 10,
    largura_centimetros: 10,
    peso_produto_gramas: 100 // Ajustado para bater com o banco
  };

  try {
    const response = await fetch(`http://127.0.0.1:8000/produtos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(novo)
    });
    const data = await response.json();
    setProdutos([data, ...produtos]); // Adiciona no topo da lista
  } catch (error) {
    alert("Erro ao adicionar.");
  }
};

const editarProduto = async (produto) => {
  const novoNome = prompt("Novo nome do produto:", produto.nome_produto);
  const novaCategoria = prompt("Nova categoria:", produto.categoria_produto);

  if (!novoNome || !novaCategoria) return;

  const dadosAtualizados = {
    ...produto, // Mantém o que não mudar
    nome_produto: novoNome,
    categoria_produto: novaCategoria,
  };

  try {
    const response = await fetch(`http://127.0.0.1:8000/produtos/${produto.id_produto}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(dadosAtualizados)
    });

    if (response.ok) {
      const produtoEditado = await response.json();
      // Atualiza o estado para refletir na tela na hora
      setProdutos(produtos.map(p => p.id_produto === produto.id_produto ? produtoEditado : p));
      alert("Produto atualizado com sucesso!");
    }
  } catch (error) {
    alert("Erro ao atualizar produto.");
  }
};

  return (
    <div className="container">
      <h1>📦 Catálogo de Produtos</h1>
      <button className="add-button" onClick={adicionarProduto}>+ Novo Produto</button>

      <div className="search-container">
        <input
          type="text"
          placeholder="Pesquisar por nome ou categoria..."
          className="search-input"
          value={busca}
          onChange={(e) => setBusca(e.target.value)}
        />
      </div>
      
      <div className="grid">
        {produtos.map((p) => (
          <div key={p.id_produto} className="card">
            <h3>{p.nome_produto}</h3>
            <p className="categoria-label">{p.categoria_produto}</p>
            
            <button className="details-button" onClick={() => abrirDetalhes(p.id_produto)}>
              Ver Detalhes
            </button>
            <button className="delete-btn" onClick={() => removerProduto(p.id_produto)}>Excluir</button>
            <button className="edit-btn" onClick={() => editarProduto(p)}>Editar</button>
          </div>
          
          
        ))}
      </div>

      {!carregando && produtos.length >= ITENS_POR_PAGINA && (
        <button className="load-more" onClick={() => {
          const p = pagina + 1; 
          setPagina(p); 
          fetchProdutos(busca, p);
        }}>
          Carregar Mais
        </button>
      )}

      {/* --- MODAL DE DETALHES (SEM O PESO) --- */}
      {detalhesProduto && (
        <div className="modal-overlay" onClick={() => setDetalhesProduto(null)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setDetalhesProduto(null)}>×</button>
            <h2>{detalhesProduto.produto.nome_produto}</h2>
            <p className="modal-categoria">{detalhesProduto.produto.categoria_produto}</p>
            <hr />
            <div className="modal-body">
              <p><strong>⭐ Média de Avaliações:</strong> {detalhesProduto.media}</p>
              <p><strong>📈 Total de Vendas:</strong> {detalhesProduto.vendas} unidades</p>
              <p><strong>📏 Medidas:</strong> {detalhesProduto.produto.comprimento_centimetros}cm (C) x {detalhesProduto.produto.altura_centimetros}cm (A)</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App