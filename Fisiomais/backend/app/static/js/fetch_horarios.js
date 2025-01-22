async function fetchHorarios(colaboradorId, dataEscolhida) {
    try {
        console.log("Buscando horários para o colaborador:", colaboradorId, "na data:", dataEscolhida);

        const response = await fetch(`/core/horarios-disponiveis/${colaboradorId}/?data=${dataEscolhida}`);
        const data = await response.json();

        console.log("Resposta recebida do backend:", data);

        const horaSelect = document.getElementById('hora');
        horaSelect.innerHTML = '<option value="" disabled selected>Selecione um horário</option>';

        if (data.horarios_disponiveis && data.horarios_disponiveis.length > 0) {
            data.horarios_disponiveis.forEach(hora => {
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
