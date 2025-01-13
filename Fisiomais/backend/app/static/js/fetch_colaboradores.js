async function fetchColaboradores(servicoId, clinicaId) {
    try {
        const response = await fetch(`/usuarios/colaboradores/?servico_id=${servicoId}&clinica_id=${clinicaId}`);
        const data = await response.json();
        const colaboradorSelect = document.getElementById('colaborador');
        colaboradorSelect.innerHTML = '<option value="" disabled selected>Selecione um colaborador</option>';
        data.colaboradores.forEach(colaborador => {
            const option = document.createElement('option');
            option.value = colaborador.id;
            option.textContent = colaborador.nome;
            colaboradorSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Erro ao buscar colaboradores:', error);
    }
}
