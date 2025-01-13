async function fetchPlanos(servicoId) {
    try {
        const response = await fetch(`/core/planos/${servicoId}/`);
        const data = await response.json();

        const planosSelect = document.getElementById('planos');
        planosSelect.innerHTML = '<option value="" disabled selected>Selecione um plano</option>';

        if (data.planos && data.planos.length > 0) {
            data.planos.forEach(plano => {
                const option = document.createElement('option');
                option.value = plano[0];  // Usar o valor do índice do plano
                option.textContent = plano[1]; // Exibir a descrição do plano
                planosSelect.appendChild(option);
            });
        } else {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'Nenhum plano disponível';
            planosSelect.appendChild(option);
        }
    } catch (error) {
        console.error('Erro ao buscar planos:', error);
    }
}