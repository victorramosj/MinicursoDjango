import React, { useState, useEffect } from "react";
import EditarServicoModal from "./EditarServicoModal";
import AddColaboradoresServicos from "./AddColaboradoresServicos";
import { FaUserPlus, FaEdit, FaTrashAlt } from "react-icons/fa";
import Paginator from "./Paginator"; // Importe o componente Paginator


const GerenciarServicos = () => {
  const [servicos, setServicos] = useState([]);
  const [colaboradores, setColaboradores] = useState([]);
  const [novoServico, setNovoServico] = useState({
    nome_servico: "",
    descricao: "",
    valor: "",
    tipo_servico: "",
    planos: [],
    colaboradores_ids: [],
  });
  const [novoPlano, setNovoPlano] = useState({ nome: "", valor: "" });
  const [erro, setErro] = useState("");
  const [mensagem, setMensagem] = useState("");
  const [modalColaboradoresVisible, setModalColaboradoresVisible] = useState(false);
  const [modalServicoVisible, setModalServicoVisible] = useState(false);
  const [selectedServico, setSelectedServico] = useState(null);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: null });
  const [tipoAlternado, setTipoAlternado] = useState(true);
  const [pesquisaNome, setPesquisaNome] = useState("");
  const [currentPage, setCurrentPage] = useState(1);  // State for current page
  const [itemsPerPage] = useState(10);  // Number of items per page


  const buscarServicos = async () => {
    try {
      const token = localStorage.getItem('token');  // Supondo que o token JWT esteja armazenado no localStorage
      const response = await fetch('http://localhost:5000/servicos/listar_todos_servicos', {
        headers: {
          'Authorization': `Bearer ${token}`  // Envia o token JWT no cabeçalho
        }
      });

      if (response.ok) {
        const servicosData = await response.json();
        setServicos(servicosData);
      } else {
        console.error('Erro ao buscar serviços: ', response.status);
      }
    } catch (error) {
      console.error('Erro ao buscar serviços:', error);
    }
  };


  const buscarUsuarios = async () => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch("http://localhost:5000/usuarios/listar_usuarios", {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        setErro("Erro ao buscar usuários: " + response.statusText);
        return;
      }

      const data = await response.json();
      const colaboradores = data.filter((usuario) => usuario.role === "colaborador");
      setColaboradores(colaboradores);
    } catch (err) {
      setErro("Erro ao buscar usuários.");
    }
  };

  useEffect(() => {
    buscarServicos();
    buscarUsuarios();
  }, []);

  const salvarServico = async () => {
    if (!novoServico.nome_servico || !novoServico.descricao || !novoServico.tipo_servico) {
      setErro("Preencha todos os campos obrigatórios do serviço.");
      return;
    }

    if (novoServico.tipo_servico === "pilates" && novoServico.planos.length === 0) {
      setErro("Serviços de Pilates precisam ter ao menos um plano.");
      return;
    }

    try {
      // Adiciona um campo 'nome_plano' para cada plano antes de enviar para o backend
      const planos = novoServico.planos.map(plano => ({
        nome_plano: plano.Nome_plano,
        valor: plano.Valor,
      }));

      // Preparando o objeto para envio
      const servicoData = {
        nome_servico: novoServico.nome_servico,
        descricao: novoServico.descricao,
        valor: novoServico.valor,  // Fisioterapia vai enviar um valor
        tipo_servico: novoServico.tipo_servico,
        colaboradores_ids: novoServico.colaboradores_ids,
        planos: planos,  // Inclui os planos formatados
      };

      const response = await fetch("http://localhost:5000/servicos/add_servico", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(servicoData),
      });

      const data = await response.json();

      if (response.ok) {
        // Atualiza a lista de serviços localmente
        setServicos((prev) => [...prev, data.servico]);
        resetForm();
        setMensagem(data.message);
        // Recarrega os serviços para garantir que a lista está atualizada
        buscarServicos();
      } else {
        throw new Error(data.error || "Erro ao salvar serviço.");
      }
    } catch (err) {
      setErro(err.message);
    }
  };


  const resetForm = () => {
    setNovoServico({
      nome_servico: "",
      descricao: "",
      valor: "",
      tipo_servico: "",
      planos: [],
      colaboradores_ids: [],
    });
    setNovoPlano({ nome: "", valor: "" });
  };

  const adicionarPlano = () => {
    if (!novoPlano.nome || !novoPlano.valor) {
      setErro("Preencha os campos Nome e Valor do plano.");
      return;
    }

    setNovoServico((prev) => ({
      ...prev,
      planos: [...prev.planos, { Nome_plano: novoPlano.nome, Valor: parseFloat(novoPlano.valor) }],
    }));

    setNovoPlano({ nome: "", valor: "" });
    setErro("");
  };

  const deletarServico = async (idServico) => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        setErro("Token não encontrado.");
        return;
      }

      const response = await fetch(`http://localhost:5000/api/deletar_servico/${idServico}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      });

      const data = await response.json();
      if (response.ok) {
        setServicos((prev) => [...prev, data.servico]);
        resetForm();
        setMensagem(data.message);
        buscarServicos();  // Recarrega a lista dos serviços caso precise
      }
      else {
        throw new Error(data.message || "Erro ao deletar serviço.");
      }
    } catch (err) {
      setErro(err.message);
    }
  };

  const handleTipoServicoChange = (e) => {
    const tipo = e.target.value;
    setNovoServico((prev) => ({
      ...prev,
      tipo_servico: tipo,
      planos: tipo === "pilates" ? [] : prev.planos,
    }));
  };

  const abrirModalColaboradores = (servico) => {
    setSelectedServico(servico);
    setModalColaboradoresVisible(true);
  };

  const abrirModalEditarServico = (servico) => {
    setSelectedServico(servico);
    setModalServicoVisible(true);
  };

  const fecharModalColaboradores = () => {
    setModalColaboradoresVisible(false);
    setSelectedServico(null);
    buscarServicos();

  };

  const fecharModalEditarServico = () => {
    setModalServicoVisible(false);
    setSelectedServico(null);
    buscarServicos();

  };

  const toggleTipo = () => {
    setTipoAlternado(!tipoAlternado);
  };
  const sortedServicos = React.useMemo(() => {
    let sorted = [...servicos];
    if (sortConfig.key && sortConfig.direction) {
      sorted.sort((a, b) => {
        const aValue = a[sortConfig.key];
        const bValue = b[sortConfig.key];

        if (typeof aValue === "string" && typeof bValue === "string") {
          const aStr = aValue.toLowerCase();
          const bStr = bValue.toLowerCase();
          if (aStr < bStr) return sortConfig.direction === "ascending" ? -1 : 1;
          if (aStr > bStr) return sortConfig.direction === "ascending" ? 1 : -1;
        } else if (typeof aValue === "number" && typeof bValue === "number") {
          if (aValue < bValue) return sortConfig.direction === "ascending" ? -1 : 1;
          if (aValue > bValue) return sortConfig.direction === "ascending" ? 1 : -1;
        }
        return 0;
      });
    }
    return sorted;
  }, [servicos, sortConfig]);

  const handleSort = (key) => {
    let direction = "ascending";
    if (sortConfig.key === key && sortConfig.direction === "ascending") {
      direction = "descending";
    }
    setSortConfig({ key, direction });
  };

  const servicosFiltrados = sortedServicos.filter((servico) => {
    const nomeServico = servico.Nome_servico || '';  // Fallback para string vazia se undefined ou null
    const tipos = servico.Tipos || []; // Garante que tipos seja um array
    return (
      nomeServico.toLowerCase().includes(pesquisaNome.toLowerCase()) &&
      (tipoAlternado
        ? tipos.includes('fisioterapia')
        : tipos.includes('pilates'))
    );
  });



  // Paginação dos usuários filtrados
  const servicosPaginados = servicosFiltrados.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );


  return (
    <div className="container">
      <h2 className="mb-4 text-secondary text-center">Gerenciar Serviços</h2>
      {erro && <div className="alert alert-danger">{erro}</div>}
      {mensagem && <div className="alert alert-success">{mensagem}</div>}

      <form
        onSubmit={(e) => {
          e.preventDefault();
          salvarServico();
        }}
        className="mb-4"
      >
        <input
          type="text"
          placeholder="Nome do Serviço"
          value={novoServico.nome_servico}
          onChange={(e) => setNovoServico({ ...novoServico, nome_servico: e.target.value })}
          required
          className="form-control mb-2"
        />
        <input
          type="text"
          placeholder="Descrição"
          value={novoServico.descricao}
          onChange={(e) => setNovoServico({ ...novoServico, descricao: e.target.value })}
          required
          className="form-control mb-2"
        />

        <select
          value={novoServico.tipo_servico}
          onChange={handleTipoServicoChange}
          className="form-control mb-2"
        >
          <option value="">Selecione o Tipo de Serviço</option>
          <option value="fisioterapia">Fisioterapia</option>
          <option value="pilates">Pilates</option>
        </select>
        {novoServico.tipo_servico === "fisioterapia" && (
          <input
            type="number"
            placeholder="Valor"
            value={novoServico.valor}
            onChange={(e) => setNovoServico({ ...novoServico, valor: e.target.value })}
            className="form-control mb-2"
          />
        )}
        {novoServico.tipo_servico === "pilates" && (
          <>
            <input
              type="text"
              placeholder="Nome do Plano"
              value={novoPlano.nome}
              onChange={(e) => setNovoPlano({ ...novoPlano, nome: e.target.value })}
              className="form-control mb-2"
            />
            <input
              type="number"
              placeholder="Valor do Plano"
              value={novoPlano.valor}
              onChange={(e) => setNovoPlano({ ...novoPlano, valor: e.target.value })}
              className="form-control mb-2"
            />
            <div className="d-flex justify-content-center">
              <button type="button" onClick={adicionarPlano} className="btn btn-signup ">
                Adicionar Plano
              </button>
            </div>
            {novoServico.planos.length > 0 && (
              <div className="mb-3">
                <label className="form-label">Planos Adicionados:</label>
                <div className="row">
                  {novoServico.planos.map((plano, index) => (
                    <div key={index} className="col-md-4 mb-4">
                      <div className="d-flex justify-content-between align-items-center p-3 border btn-plano rounded">
                        <div className="flex-grow-1">
                          <strong>{plano.Nome_plano}</strong>
                        </div>
                        <div className="text-end">
                          <span className="fw-bold">R$ {plano.Valor.toFixed(2)}</span>
                        </div>
                        <button
                          type="button"
                          onClick={() =>
                            setNovoServico((prev) => ({
                              ...prev,
                              planos: prev.planos.filter((_, i) => i !== index),
                            }))
                          }
                          className="btn btn-danger btn-sm ms-2"
                        >
                          <i className="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}


        <div className="d-flex justify-content-center">
          <button type="submit" className="btn btn-login mt-3">Adicionar Serviço</button>
        </div>
      </form>

      <h3 className="text-primary">Lista de Serviços</h3>
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control"
          placeholder="Pesquisar por nome do serviço"
          value={pesquisaNome}
          onChange={(e) => setPesquisaNome(e.target.value)}
        />
        <button className="btn btn-secondary" type="button" id="button-addon2">
          <i className="bi bi-search"></i>
        </button>
      </div>
      <div className="table-responsive ">
        <table className="table table-striped table-bordered mt-4">
          <thead>
            <tr>
              <th
                onClick={() => handleSort("Nome_servico")}
                style={{ cursor: "pointer" }}
              >
                Nome
                {sortConfig.key === "Nome_servico" && (sortConfig.direction === "ascending" ? " ↑" : " ↓")}
              </th>
              <th>Descrição</th>
              <th>Valor (R$)</th>
              <th onClick={toggleTipo} style={{ cursor: "pointer" }}>
                Tipo <small>(clique)</small>< br/> {tipoAlternado ? "Fisioterapia" : "Pilates"}
              </th>
              <th>Planos</th>
              <th>Colaboradores</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            {servicosPaginados.map((servico) => (
              <tr key={servico.ID_Servico}>
                <td>{servico.Nome_servico}</td>
                <td>{servico.Descricao}</td>
                <td>{servico.Valor ? `R$ ${parseFloat(servico.Valor).toFixed(2)}` : '-'}</td>
                <td className="text-center">{servico.Tipos[0].charAt(0).toUpperCase() + servico.Tipos[0].slice(1)}</td>
                <td >
                  {servico.Tipos.includes("pilates") && servico.Planos && servico.Planos.length > 0 ? (
                    <ul className="list-unstyled text-center">
                      {servico.Planos.map((plano, index) => (
                        <li key={index}>
                          {plano.Nome_plano} - R${parseFloat(plano.Valor).toFixed(2)}
                        </li>
                      ))}
                    </ul>
                  ) : (
                    servico.Tipos.includes("pilates") ? "Nenhum plano adicionado" : <span className="d-block">-</span>
                  )}
                </td>
                <td>
                  {servico.Colaboradores && servico.Colaboradores.length > 0
                    ? servico.Colaboradores.join(", ")
                    : "Nenhum colaborador"}
                </td>
                <td >
                  <div className="d-flex justify-content-start align-items-center align-middle border-0 ">
                    <button
                      className="btn btn-primary btn-sm ms "
                      onClick={() => abrirModalEditarServico(servico)}
                    >
                      <FaEdit className="fs-7" />
                    </button>
                    <button
                      className="btn btn-info btn-sm ms-2"
                      onClick={() => abrirModalColaboradores(servico)}
                    >
                      <FaUserPlus className="fs-7" />
                    </button>
                    <button
                      className="btn btn-danger btn-sm ms-2"
                      onClick={() => deletarServico(servico.ID_Servico)}
                    >
                      <FaTrashAlt className="fs-7" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      <Paginator
        totalItems={servicosFiltrados.length}
        itemsPerPage={itemsPerPage}
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
      />

      {modalServicoVisible && selectedServico && (
        <EditarServicoModal
          servico={selectedServico}
          onSave={(updatedServico) => {
            setServicos((prev) =>
              prev.map((s) => (s.ID_Servico === updatedServico.ID_Servico ? updatedServico : s))
            );
            fecharModalEditarServico();
          }}

          onClose={fecharModalEditarServico}
        />
      )}

      {modalColaboradoresVisible && selectedServico && (
        <AddColaboradoresServicos
          servicoId={selectedServico.ID_Servico}
          onSave={(colaboradoresSelecionados) => {
            setServicos((prev) =>
              prev.map((s) =>
                s.ID_Servico === selectedServico.ID_Servico
                  ? { ...s, Colaboradores: colaboradoresSelecionados }
                  : s
              )
            );
            fecharModalColaboradores();
          }}
          onClose={fecharModalColaboradores}
        />
      )}
    </div>
  );
};

export default GerenciarServicos;
