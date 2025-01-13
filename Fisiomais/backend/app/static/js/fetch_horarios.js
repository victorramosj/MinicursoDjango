async function fetchHorarios(colaboradorId, dataEscolhida) {
    try {
        const response = await fetch(`/core/horarios-disponiveis/${colaboradorId}/?data=${dataEscolhida}`);
        const data = await response.json();
        const horaSelect = document.getElementById('hora');
        horaSelect.innerHTML = '<option value="" disabled selected>Selecione um horário</option>';

        if (data.horarios_disponiveis && data.horarios_disponiveis.length > 0) {
            const horariosUnicos = [...new Set(data.horarios_disponiveis)];

            horariosUnicos.forEach(hora => {
                const option = document.createElement('option');
                option.value = hora;
                option.textContent = hora;
                horaSelect.appendChild(option);
            });
        } else {
            const option = document.createElement('option');
            option.value = '';
            option.textContent = 'Nenhum horário disponível';
            horaSelect.appendChild(option);
        }
    } catch (error) {
        console.error('Erro ao buscar horários:', error);
    }
}
