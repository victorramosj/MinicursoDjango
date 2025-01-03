import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";
import "../css/Navbar.css";
import CadastroClienteModal from './CadastroClienteModal'; // Atualize o caminho conforme necessário

function Navbar() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userName, setUserName] = useState("Usuário");
  const [role, setRole] = useState("");
  const [email, setEmail] = useState("");
  const [senha, setPassword] = useState("");
  const [userId, setUserId] = useState(null);
  const [userPhoto, setUserPhoto] = useState("");
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [emailConfirmed, setEmailConfirmed] = useState(true);
  const [rememberMe, setRememberMe] = useState(false);
  const [isEmailConfirmed, setIsEmailConfirmed] = useState(false); // Inicialmente assumimos que não está confirmado
  const [showCadastroModal, setShowCadastroModal] = useState(false);

  const navigate = useNavigate();


  const handleLogin = async () => {
    try {
      const response = await axios.post("http://localhost:8000/login/", { email, senha });
      const { access_token, name, role, userId, photo, email_confirmado } = response.data;

      // Armazenar os dados no estado e no localStorage
      setIsLoggedIn(true);
      setUserName(name);
      setRole(role);
      setUserId(userId);
      setUserPhoto(photo || "");
      setEmailConfirmed(email_confirmado);

      // Armazenar as informações no localStorage
      localStorage.setItem("token", access_token);
      localStorage.setItem("userName", name);
      localStorage.setItem("role", role);
      localStorage.setItem("userId", userId);
      localStorage.setItem("userPhoto", photo || "");
      localStorage.setItem("email_confirmado", email_confirmado.toString());
      localStorage.setItem("isLoggedIn", "true"); // Armazenar isLoggedIn

      // Fecha o modal de login
      const modalElement = document.getElementById("loginModal");
      const modalInstance = window.bootstrap.Modal.getInstance(modalElement);
      if (modalInstance) modalInstance.hide();
      document.querySelectorAll(".modal-backdrop").forEach((backdrop) => backdrop.remove());

      // Redireciona com base no papel do usuário
      setTimeout(() => {
        navigate(role === "admin" ? "/adminpage" : "/");
        window.location.reload();
      }, 300);

      // Inicia a renovação automática do token
      autoRefreshToken();
    } catch (error) {
      console.error("Erro no login:", error);
      alert("Erro ao fazer login. Verifique suas credenciais.");
    }
  };

  const handleCadastroSuccess = (data) => {
    console.log('Dados recebidos no cadastro:', data);

    if (data && data.userId && data.name && data.role && data.email) {
      // Atualizando o estado de forma individual
      setIsLoggedIn(true);
      setUserName(data.name);
      setRole(data.role);
      setUserId(data.userId);
      setUserPhoto(data.photo || "");
      setEmailConfirmed(data.email_confirmado);

      // Persistindo as informações no localStorage
      localStorage.setItem('token', data.access_token); // Correção aqui
      localStorage.setItem('userName', data.name);
      localStorage.setItem('role', data.role);
      localStorage.setItem('userId', data.userId);
      localStorage.setItem('userPhoto', data.photo || "");
      localStorage.setItem('email_confirmado', data.email_confirmado ? "true" : "false");
      localStorage.setItem('isLoggedIn', 'true');

      setShowCadastroModal(false);

      navigate("/criarAgendamento");
    } else {
      console.error('Erro: Dados incompletos ou ausentes', data);
      alert("Erro ao cadastrar o usuário. Tente novamente.");
    }
  };


  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    const storedIsLoggedIn = localStorage.getItem("isLoggedIn");
    const storedIsEmailConfirmed = localStorage.getItem("email_confirmado");

    if (storedToken && storedIsLoggedIn === "true") {
      setIsLoggedIn(true);
    }

    if (storedIsEmailConfirmed) {
      setIsEmailConfirmed(storedIsEmailConfirmed === "true");
    }
  }, []);







  // Função para renovar o token automaticamente
  const autoRefreshToken = () => {
    const refreshInterval = 1 * 60 * 1000; // 10 minutos
    const sessionEndTime = 60 * 60 * 1000; // 1 hora


    const refreshToken = async () => {
      try {
        const storedRefreshToken = localStorage.getItem("refresh_token");
        if (!storedRefreshToken) return;

        const response = await axios.post(
          "http://localhost:5000/refresh-token",
          {},
          { headers: { Authorization: `Bearer ${storedRefreshToken}` } }
        );

        if (response.data.access_token) {
          localStorage.setItem("token", response.data.access_token);
        }
      } catch (error) {
        console.error("Erro ao renovar o token:", error.response?.data?.message || "Erro desconhecido");
        alert("Sua sessão expirou. Faça login novamente.");
        handleLogout();
      }
    };

    const intervalId = setInterval(refreshToken, refreshInterval);
    const logoutTimeout = setTimeout(handleLogout, sessionEndTime);

    return () => {
      clearInterval(intervalId);
      clearTimeout(logoutTimeout);
    };
  };



  // Função para realizar logout
  const handleLogout = async () => {
    try {
      const savedToken = localStorage.getItem("token");
      if (savedToken) {
        await axios.post("http://localhost:5000/logout", {}, {
          headers: { Authorization: `Bearer ${savedToken}` },
        });
      }
    } catch (error) {
      console.error("Erro no logout:", error);
    } finally {
      localStorage.clear();
      setIsLoggedIn(false);
      setUserName("Usuário");
      setRole("");
      setUserId(null);
      setUserPhoto("");
      navigate("/");
    }
  };

  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedUserName = localStorage.getItem("userName");
    const savedRole = localStorage.getItem("role");
    const savedUserId = localStorage.getItem("userId");
    const savedUserPhoto = localStorage.getItem("userPhoto");

    if (savedToken && savedUserName && savedRole) {
      try {
        const decodedToken = JSON.parse(atob(savedToken.split(".")[1]));
        const isTokenExpired = decodedToken.exp * 1000 < Date.now();
        if (isTokenExpired) throw new Error("Token expirado");

        setIsLoggedIn(true);
        setUserName(savedUserName);
        setRole(savedRole);
        setUserId(savedUserId);
        setUserPhoto(savedUserPhoto || "");
      } catch (error) {
        console.error("Erro ao verificar o token:", error);
        handleLogout();
      }
    }
  }, []);

  useEffect(() => {
    const cleanup = autoRefreshToken();
    return cleanup; // Limpa os temporizadores ao desmontar
  }, []);


  return (
    <>

      <nav className="navbar navbar-expand-lg navbar-light bg-light">
        <div className="container-fluid">
          <Link className="navbar-brand" to="/">
            <img src="/fisiomais.png" alt="Logo" className="navbar-logo" />
          </Link>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav mx-auto">
              <li className="nav-item">
                <Link className="nav-link" to="/">Início</Link>
              </li>

              <li className="nav-item">
                <Link className="nav-link" to="/sobrenos">Sobre Nós</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/especialidades">Especialidades</Link>
              </li>
              <li className="nav-item">
                <Link className="nav-link" to="/contato">Fale conosco</Link>
              </li>
              {isLoggedIn && role !== "cliente" && (
                <li className="nav-item">
                  <Link className="nav-link" to="/adminPage">Central de Controle</Link>
                </li>
              )}

            </ul>


            <ul className={`navbar-nav ms-auto ${isLoggedIn ? 'z-top' : ''}`}>
              {!isLoggedIn ? (
                <>
                  <li className="nav-item  ">
                    <button
                      className="btn btn-login d-flex align-items-center gap-2"
                      data-bs-toggle="modal"
                      data-bs-target="#loginModal"
                    >
                      <i className="bi bi-box-arrow-in-right"> </i> Entrar
                    </button>
                  </li>
                  <li className="nav-item">
                    <button
                      className="btn btn-signup align-items-center gap-2"
                      onClick={() => setShowCadastroModal(true)} // Abre o modal ao clicar no botão
                    >
                      <i className="bi bi-person-plus"></i> Inscrever-se
                    </button>
                  </li>
                </>
              ) : (

                <li className="nav-item dropdown  btn-user">
                  <a
                    className="nav-link dropdown-toggle   btn-user"
                    href="#"
                    id="navbarDropdown"
                    role="button"
                    data-bs-toggle="dropdown"

                    aria-expanded="false"
                  >
                    {userPhoto && userPhoto.trim() !== "" ? (
                      <img
                        src={`http://localhost:5000/usuarios/uploads/${userPhoto}?t=${new Date().getTime()}`}
                        alt="Foto de perfil"
                        className="user-photo"
                      />
                    ) : (
                      <i id="iconeuser" className="bi bi-person-circle"></i> // Exibe o ícone se não houver foto
                    )}
                    <span>{userName}</span>
                  </a>
                  <ul className="dropdown-menu" aria-labelledby="navbarDropdown">
                    <li>
                      <Link className="dropdown-item" to="/perfil">Meu Perfil</Link>
                    </li>
                    <li>
                      <Link className="dropdown-item" to="/criaragendamento">Agendar Atendimento</Link>
                    </li>

                    {role === "admin" && (
                      <>
                        <li>
                          <Link className="dropdown-item" to="/adminPage">Pagina Administrador</Link>
                        </li>
                      </>
                    )}
                    {role === "colaborador" && (
                      <li>
                        <Link className="dropdown-item" to="/adminPage">Central de Controle</Link>
                      </li>
                    )
                    }


                    <li>
                      <Link className="dropdown-item" to="/visualizaragendamentos">Agendamentos</Link>
                    </li>
                    <li>
                      <button
                        className="dropdown-item"
                        onClick={handleLogout}
                        type="button"

                      >
                        Sair
                      </button>
                    </li>

                  </ul>
                </li>

              )}
            </ul>
          </div>
        </div>
      </nav>
      {isLoggedIn && !isEmailConfirmed && (
        <div className="container-fluid mt-2">
          <div className="alert alert-warning alert-dismissible fade show text-center z-bot" role="alert">
            <strong>Atenção!</strong> E-mail não confirmado. Por favor, verifique seu e-mail.
            <button
              type="button"
              className="btn-close"
              data-bs-dismiss="alert"
              aria-label="Close"
            ></button>
          </div>
        </div>
      )}

      {/* Modal de Cadastro */}
      <CadastroClienteModal
        show={showCadastroModal}
        onHide={() => setShowCadastroModal(false)} // Fecha o modal
        onRegisterSuccess={handleCadastroSuccess} // Lida com o sucesso do cadastro
      />
      {/* Modal de Login */}
      <div
        className="modal fade"
        id="loginModal"
        tabIndex="-1"
        aria-labelledby="loginModalLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header text-center justify-content-center">
              <h5 className="modal-title  d-flex align-items-center gap-2" id="loginModalLabel">
                <i className="bi  bi-person-circle"></i>
                Login
              </h5>
              <button
                type="button"
                className="btn-close"
                data-bs-dismiss="modal"
                aria-label="Close"
              ></button>
            </div>
            <div className="modal-body">
              <form onSubmit={(e) => e.preventDefault()}>
                <div className="mb-2">
                  <label htmlFor="email" className="form-label ">
                    <i className="bi bi-envelope"></i> Email
                  </label>
                  <input
                    type="email"
                    className="form-control"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="mb-2">
                  <label htmlFor="senha" className="form-label">
                    <i className="bi bi-lock"></i> Senha
                  </label>
                  <div className="input-group">
                    <input
                      type={mostrarSenha ? "text" : "password"}
                      className="form-control"
                      id="senha"
                      value={senha}
                      onChange={(e) => setPassword(e.target.value)}
                      required
                    />
                    <button
                      type="button"
                      className="btn btn-outline-secondary"
                      onClick={() => setMostrarSenha(!mostrarSenha)}
                    >
                      {mostrarSenha ? (
                        <i className="bi bi-eye-slash"></i>
                      ) : (
                        <i className="bi bi-eye"></i>
                      )}
                    </button>
                  </div>
                </div>
                <div className="d-flex justify-content-between align-items-center mb-3">
                  <div>
                    <input
                      type="checkbox"
                      id="rememberMe"
                      checked={rememberMe}
                      onChange={() => setRememberMe(!rememberMe)}
                    />
                    <label htmlFor="rememberMe"> Lembre-me</label>
                  </div>
                  <a href="#" className="">
                    <i className="bi bi-arrow-clockwise"></i> Esqueceu a senha?
                  </a>
                </div>
                <button
                  type="submit"
                  className="btn btn btn-signup w-100"
                  onClick={handleLogin}
                >
                  <i className="bi bi-box-arrow-in-right"></i> Entrar
                </button>
              </form>
            </div>
            <div className="modal-footer">
              <p>
                Não tem uma conta?{" "}
                <button
                  className="btn text-white"
                  onClick={() => {
                    // Fecha o modal de login, se estiver aberto
                    const modalElement = document.getElementById("loginModal");
                    const modalInstance = window.bootstrap.Modal.getInstance(modalElement);
                    if (modalInstance) modalInstance.hide();
                    document.querySelectorAll(".modal-backdrop").forEach((backdrop) => backdrop.remove());

                    // Abre o modal de cadastro
                    setShowCadastroModal(true);
                  }}
                >
                  Inscreva-se
                </button>
              </p>
              <div className="social-icons">
                <button className="btn btn-outline-primary btn-social">
                  <i className="bi bi-facebook"></i>
                </button>
                <button className="btn btn-outline-danger btn-social">
                  <i className="bi bi-google"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

    </>
  );
}

export default Navbar;