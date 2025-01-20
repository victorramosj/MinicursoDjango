// Função para carregar os estados
function loadEstados(estadoSelectId) {
    fetch('/usuarios/estados/')
        .then(response => response.json())
        .then(data => {
            const estadoSelect = document.getElementById(estadoSelectId);
            estadoSelect.innerHTML = '<option value="">Selecione um Estado</option>'; // Limpa qualquer opção anterior
            if (Array.isArray(data)) {
                data.forEach(estado => {
                    const option = document.createElement("option");
                    option.value = estado.sigla;
                    option.textContent = estado.nome;
                    estadoSelect.appendChild(option);
                });
            }
            // Log para colaborador
            if (estadoSelectId === "id_estado_cadastro_colaborador") {
                console.log("Estados carregados para o cadastro de colaborador:", data);
            }
        })
        .catch(error => {
            console.error("Erro ao carregar estados:", error);
            // Log para colaborador
            if (estadoSelectId === "id_estado_cadastro_colaborador") {
                console.error("Erro ao carregar estados para o cadastro de colaborador:", error);
            }
        });
}

// Função para carregar as cidades com base no estado selecionado
function loadCidades(estado, cidadeSelectId) {
    const url = `/usuarios/cidades/${estado}/`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const cidadeSelect = document.getElementById(cidadeSelectId);
            cidadeSelect.innerHTML = '<option value="">Selecione uma Cidade</option>'; // Limpa qualquer opção anterior
            if (Array.isArray(data)) {
                data.forEach(cidade => {
                    const option = document.createElement("option");
                    option.value = cidade.nome;
                    option.textContent = cidade.nome;
                    cidadeSelect.appendChild(option);
                });
            }
            // Log para colaborador
            if (cidadeSelectId === "id_cidade_cadastro_colaborador") {
                console.log(`Cidades carregadas para o estado ${estado} no cadastro de colaborador:`, data);
            }
        })
        .catch(error => {
            console.error("Erro ao carregar cidades:", error);
            // Log para colaborador
            if (cidadeSelectId === "id_cidade_cadastro_colaborador") {
                console.error(`Erro ao carregar cidades para o estado ${estado} no cadastro de colaborador:`, error);
            }
        });
}

// Carregar os estados ao carregar a página
document.addEventListener("DOMContentLoaded", function () {
    const estadoSelectCliente = document.getElementById("id_estado_cadastro_cliente");
    if (estadoSelectCliente) {
        estadoSelectCliente.addEventListener("change", function () {
            const estadoSelecionado = estadoSelectCliente.value;
            const cidadeSelectCliente = document.getElementById("id_cidade_cadastro_cliente");
            if (estadoSelecionado) {
                loadCidades(estadoSelecionado, "id_cidade_cadastro_cliente");
            } else {
                cidadeSelectCliente.innerHTML = '<option value="">Selecione uma Cidade</option>';
            }
        });
        loadEstados("id_estado_cadastro_cliente");
    }

    const estadoSelectColaborador = document.getElementById("id_estado_cadastro_colaborador");
    if (estadoSelectColaborador) {
        estadoSelectColaborador.addEventListener("change", function () {
            const estadoSelecionado = estadoSelectColaborador.value;
            const cidadeSelectColaborador = document.getElementById("id_cidade_cadastro_colaborador");
            if (estadoSelecionado) {
                loadCidades(estadoSelecionado, "id_cidade_cadastro_colaborador");
            } else {
                cidadeSelectColaborador.innerHTML = '<option value="">Selecione uma Cidade</option>';
            }
        });
        loadEstados("id_estado_cadastro_colaborador");
    }
});

