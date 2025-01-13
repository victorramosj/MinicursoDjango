async function fetchServicos() {
    try {
        const response = await fetch('/core/get_servicos/');
        const data = await response.json();
        const servicoSelect = document.getElementById('servico');
        const valorInput = document.getElementById('valor');
        const planosDiv = document.getElementById('planos-div');
        const valorDiv = document.getElementById('valor-div');
        servicoSelect.innerHTML = '<option value="" disabled selected>Selecione um serviço</option>';
        
        data.servicos.forEach(servico => {
            const option = document.createElement('option');
            option.value = servico.id;
            option.textContent = servico.nome_servico;
            servicoSelect.appendChild(option);
        });

        // Adiciona um listener para atualizar o valor ao selecionar um serviço
        servicoSelect.addEventListener('change', function () {
            const selectedServico = data.servicos.find(servico => servico.id == servicoSelect.value);
            if (selectedServico) {
                // Exibe ou esconde o valor e plano conforme o tipo de serviço
                if (selectedServico.tipo_servico === 'Fisioterapia') {
                    valorDiv.style.display = 'block';  // Exibe o valor
                    planosDiv.style.display = 'none';  // Esconde os planos
                    valorInput.value = selectedServico.valor; // Atualiza o valor do serviço
                } else if (selectedServico.tipo_servico === 'Pilates') {
                    valorDiv.style.display = 'none';  // Esconde o valor
                    planosDiv.style.display = 'block'; // Exibe os planos
                    // Aqui você pode fazer uma requisição para obter os planos de Pilates
                }
            }
        });

    } catch (error) {
        console.error('Erro ao buscar serviços:', error);
    }
}
