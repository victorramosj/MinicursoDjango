  import React, { useState, useEffect } from 'react';
  import axios from 'axios';
  import 'bootstrap/dist/css/bootstrap.min.css';
  import { Link } from "react-router-dom";

  function AddColaborador() {
    const [nome, setNome] = useState('');
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const [telefone, setTelefone] = useState('');
    const [cpf, setCpf] = useState('');
    const [dtNasc, setDtNasc] = useState('');
    const [rua, setRua] = useState('');
    const [numero, setNumero] = useState('');
    const [bairro, setBairro] = useState('');
    const [estado, setEstado] = useState('');
    const [cidade, setCidade] = useState('');
    const [referencias, setReferencias] = useState('');
    const [cargo, setCargo] = useState('');
    const [isAdmin, setIsAdmin] = useState(false);
    const [clinica, setClinica] = useState('');
    const [clinicas, setClinicas] = useState([]);
    const [cidades, setCidades] = useState([]);
    const [estados, setEstados] = useState([]);
    const [loading, setLoading] = useState(false);
    const [sexo, setSexo] = useState('');
    const [photo, setPhoto] = useState('');
    const [adminNivel, setAdminNivel] = useState('');


    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
      const fetchEstados = async () => {
        try {
          const response = await axios.get('https://servicodados.ibge.gov.br/api/v1/localidades/estados');
          setEstados(response.data.map((estado) => ({ sigla: estado.sigla, nome: estado.nome })));
        } catch (error) {
          console.error('Erro ao buscar estados:', error);
        }
      };

      const fetchClinicas = async () => {
        try {
          const response = await axios.get('http://localhost:5000/clinicas');
          setClinicas(response.data);
        } catch (error) {
          console.error('Erro ao buscar clínicas:', error);
        }
      };

      fetchEstados();
      fetchClinicas();
    }, []);

    useEffect(() => {
      if (estado) {
        const fetchCidades = async () => {
          try {
            const response = await axios.get(`https://servicodados.ibge.gov.br/api/v1/localidades/estados/${estado}/municipios`);
            setCidades(response.data.map((cidade) => cidade.nome).sort());
          } catch (error) {
            console.error('Erro ao buscar cidades:', error);
          }
        };

        fetchCidades();
      }
    }, [estado]);

    const handleRegister = async () => {
      setLoading(true);

      try {
        const token = localStorage.getItem('token'); // Obter o token armazenado
        console.log('Token obtido:', token);

        const payload = {
          nome,
          email,
          senha,
          telefone,
          cpf,
          dt_nasc: dtNasc || null,  // Enviar null se não houver data
          referencias,
          cargo,
          sexo: sexo || null,  // Enviar null se não houver sexo
          is_admin: isAdmin,
          endereco: { rua, numero, bairro, cidade, estado },
          clinica_id: clinica,
          photo: photo || null,  // Enviar null se não houver foto
          adminNivel: adminNivel || null,  // Enviar null se não houver nível
        };



        console.log('Payload enviado:', payload);

        const response = await axios.post(
          'http://localhost:5000/colaboradores/register',
          payload,
          {
            headers: {
              Authorization: `Bearer ${token}`, // Adicionar o token no cabeçalho
            },
          }
        );

        console.log('Resposta do servidor:', response);

        if (response.status === 201) {
          alert('Colaborador cadastrado com sucesso!');
          // Resetar os campos
          setNome('');
          setEmail('');
          setSenha('');
          setTelefone('');
          setCpf('');
          setDtNasc('');
          setRua('');
          setNumero('');
          setBairro('');
          setEstado('');
          setCidade('');
          setReferencias('');
          setCargo('');
          setIsAdmin(false);
          setClinica('');
          setPhoto('');
          setAdminNivel('');
        }
      } catch (error) {
        console.error('Erro ao cadastrar colaborador:', error);

        // Exibir a mensagem de erro retornada pelo servidor, se disponível
        if (error.response && error.response.data) {
          console.error('Detalhes do erro:', error.response.data);
          alert(`Erro ao cadastrar colaborador: ${error.response.data.error || 'Erro desconhecido'}`);
        } else {
          alert('Erro ao cadastrar colaborador.');
        }
      } finally {
        setLoading(false);
      }
    };


    return (
      <div className="container col-md-9 my-5">
        {errorMessage && <div className="alert alert-danger">{errorMessage}</div>}
        <div className="card shadow">
          <div className="card-header">
            <h2 className="text-center text-primary">Adicionar Colaborador</h2>
          </div>
          <div className="card-body">
            <form onSubmit={(e) => { e.preventDefault(); handleRegister(); }}>
              {/* Nome, Email e Senha */}
              <div className="row mb-3">
                <div className="col-md-4">
                  <label htmlFor="nome" className="form-label">Nome*</label>
                  <input
                    type="text"
                    className="form-control"
                    id="nome"
                    value={nome}
                    onChange={(e) => setNome(e.target.value)}
                    required
                  />
                </div>
                <div className="col-md-4">
                  <label htmlFor="email" className="form-label">Email*</label>
                  <input
                    type="email"
                    className="form-control"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="col-md-4">
                  <label htmlFor="senha" className="form-label">Senha*</label>
                  <input
                    type="password"
                    className="form-control"
                    id="senha"
                    value={senha}
                    onChange={(e) => setSenha(e.target.value)}
                    required
                  />
                </div>
              </div>

              {/* Telefone e CPF */}
              <div className="row mb-3">
                <div className="col-md-4">
                  <label htmlFor="telefone" className="form-label">Telefone</label>
                  <input
                    type="text"
                    className="form-control"
                    id="telefone"
                    value={telefone}
                    onChange={(e) => setTelefone(e.target.value)}
                  />
                </div>
                <div className="col-md-4">
                  <label htmlFor="cpf" className="form-label">CPF*</label>
                  <input
                    type="text"
                    className="form-control"
                    id="cpf"
                    value={cpf}
                    onChange={(e) => setCpf(e.target.value)}
                    required
                  />
                </div>
                <div className="col-md-2">
                  <label htmlFor="dtNasc" className="form-label">Data de Nascimento</label>
                  <input
                    type="date"
                    className="form-control"
                    id="dtNasc"
                    value={dtNasc}
                    onChange={(e) => setDtNasc(e.target.value)}
                  />
                </div>
                {/* Data de Nascimento */}
                <div className="col-md-2">
                  <label htmlFor="sexo" className="form-label">Sexo</label>
                  <select
                    id="sexo"
                    className="form-control"
                    value={sexo}
                    onChange={(e) => setSexo(e.target.value)}
                  >
                    <option value="">Selecione o sexo</option>
                    <option value="Masculino">Masculino</option>
                    <option value="Feminino">Feminino</option>
                    <option value="Outro">Outro</option>
                  </select>
                </div>
              </div>




              {/* Endereço */}
              <div className="row mb-3">
                <div className="col-md-4">
                  <label htmlFor="estado" className="form-label">Estado*</label>
                  <select
                    className="form-select"
                    id="estado"
                    value={estado}
                    onChange={(e) => setEstado(e.target.value)}
                    required
                  >
                    <option value="">Selecione</option>
                    {estados.map((uf) => (
                      <option key={uf.sigla} value={uf.sigla}>{uf.nome}</option>
                    ))}
                  </select>
                </div>
                <div className="col-md-4">
                  <label htmlFor="cidade" className="form-label">Cidade*</label>
                  <select
                    className="form-select"
                    id="cidade"
                    value={cidade}
                    onChange={(e) => setCidade(e.target.value)}
                    required
                  >
                    <option value="">Selecione</option>
                    {cidades.map((cidade) => (
                      <option key={cidade} value={cidade}>{cidade}</option>
                    ))}
                  </select>
                </div>
                <div className="col-md-4">
                  <label htmlFor="bairro" className="form-label">Bairro</label>
                  <input
                    type="text"
                    className="form-control"
                    id="bairro"
                    value={bairro}
                    onChange={(e) => setBairro(e.target.value)}
                  />
                </div>
              </div>

              {/* Rua e Número */}
              <div className="row mb-3">
                <div className="col-md-8">
                  <label htmlFor="rua" className="form-label">Rua</label>
                  <input
                    type="text"
                    className="form-control"
                    id="rua"
                    value={rua}
                    onChange={(e) => setRua(e.target.value)}
                  />
                </div>
                <div className="col-md-4">
                  <label htmlFor="numero" className="form-label">Número</label>
                  <input
                    type="text"
                    className="form-control"
                    id="numero"
                    value={numero}
                    onChange={(e) => setNumero(e.target.value)}
                  />
                </div>
              </div>

              {/* Cargo e Referências */}
              <div className="row mb-3">
                <div className="col-md-6">
                  <label htmlFor="cargo" className="form-label">Cargo</label>
                  <input
                    type="text"
                    className="form-control"
                    id="cargo"
                    value={cargo}
                    onChange={(e) => setCargo(e.target.value)}
                  />
                </div>
                <div className="col-md-6">
                  <label htmlFor="referencias" className="form-label">Referências</label>
                  <textarea
                    className="form-control"
                    id="referencias"
                    value={referencias}
                    onChange={(e) => setReferencias(e.target.value)}
                  />
                </div>
              </div>

              {/* Admin e Clínica */}
              <div className="row mb-3">
                <div className="col-md-5">
                  <label htmlFor="clinica" className="form-label">Clínica</label>
                  <select
                    className="form-select"
                    id="clinica"
                    value={clinica}
                    onChange={(e) => setClinica(e.target.value)}
                  >
                    <option value="">Selecione</option>
                    {clinicas.map((clinica) => (
                      <option key={clinica.ID_Clinica} value={clinica.ID_Clinica}>{clinica.Nome}</option>
                    ))}
                  </select>
                </div>
                <div className="col-md-2 d-flex align-items-center">
                  <div className="form-check">
                    <input
                      type="checkbox"
                      className="form-check-input"
                      id="isAdmin"
                      checked={isAdmin}
                      onChange={(e) => {
                        setIsAdmin(e.target.checked);
                        setAdminNivel(e.target.checked ? 'restrito' : 'geral');  // Atualiza o admin_nivel
                      }}
                    />
                    <label htmlFor="isAdmin" className="form-check-label text-dark">É Administrador?</label>
                  </div>
                </div>

                {/* Exibe o select para escolher o nível de admin quando o checkbox for marcado */}
                {isAdmin && (
                  <div className="col-md-5 ">
                    <label htmlFor="adminNivel" className="form-label">Nível de Administrador</label>
                    <select
                      id="adminNivel"
                      className="form-select"
                      value={adminNivel}
                      onChange={(e) => setAdminNivel(e.target.value)}
                    >
                      <option value="geral">Geral</option>
                      <option value="restrito">Restrito</option>
                    </select>
                  </div>
                )}

              </div>

              {/* Botão de Cadastro */}
              <div className="d-flex justify-content-end">
                <button type="submit" className="btn btn-login" disabled={loading}>
                  {loading ? 'Cadastrando...' : 'Cadastrar'}

                </button>
                <Link className="btn btn-signup   ms-2" to="/adminpage" disabled={loading}>
                  <i class="bi bi-arrow-return-left me-2"></i>
                  {loading ? "Carregando..." : "Voltar"}
                </Link>
              </div>
            </form>
          </div>
        </div>
      </div>
    );

  }

  export default AddColaborador;
