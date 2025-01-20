// Função para carregar os estados
function loadEstados(estadoSelectId) {
    fetch('/usuarios/estados/')
        .then(response => response.json())
        .then(data => {
            const estadoSelect = document.getElementById(estadoSelectId);
            estadoSelect.innerHTML = '<option value="">Selecione um Estado</option>';  // Limpa qualquer opção anterior
            if (Array.isArray(data)) {
                data.forEach(estado => {
                    const option = document.createElement("option");
                    option.value = estado.sigla;
                    option.textContent = estado.nome;
                    estadoSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error("Erro ao carregar estados:", error);
        });
}

// Função para carregar as cidades com base no estado selecionado
function loadCidades(estado, cidadeSelectId) {
    const url = `/usuarios/cidades/${estado}/`;
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const cidadeSelect = document.getElementById(cidadeSelectId);
            cidadeSelect.innerHTML = '<option value="">Selecione uma Cidade</option>';  // Limpa qualquer opção anterior
            if (Array.isArray(data)) {
                data.forEach(cidade => {
                    const option = document.createElement("option");
                    option.value = cidade.nome;
                    option.textContent = cidade.nome;
                    cidadeSelect.appendChild(option);
                });
            }
        })
        .catch(error => {
            console.error("Erro ao carregar cidades:", error);
        });
}

// Carregar os estados ao carregar a página
document.addEventListener("DOMContentLoaded", function() {
    // Passa os IDs de estado e cidade para a função para cada página
    loadEstados("id_estado_cadastro_cliente");  // Exemplo de ID para cadastro de cliente
    loadEstados("id_estado_cadastro_colaborador");  // Exemplo de ID para cadastro de colaborador

    // Atualizar as cidades quando o estado for selecionado
    const estadoSelectCliente = document.getElementById("id_estado_cadastro_cliente");
    estadoSelectCliente.addEventListener("change", function () {
        const estadoSelecionado = estadoSelectCliente.value;
        const cidadeSelectCliente = document.getElementById("id_cidade_cadastro_cliente");
        if (estadoSelecionado) {
            loadCidades(estadoSelecionado, "id_cidade_cadastro_cliente");
        } else {
            cidadeSelectCliente.innerHTML = '<option value="">Selecione uma Cidade</option>';
        }
    });

    const estadoSelectColaborador = document.getElementById("id_estado_cadastro_colaborador");
    estadoSelectColaborador.addEventListener("change", function () {
        const estadoSelecionado = estadoSelectColaborador.value;
        const cidadeSelectColaborador = document.getElementById("id_cidade_cadastro_colaborador");
        if (estadoSelecionado) {
            loadCidades(estadoSelecionado, "id_cidade_cadastro_colaborador");
        } else {
            cidadeSelectColaborador.innerHTML = '<option value="">Selecione uma Cidade</option>';
        }
    });
});

