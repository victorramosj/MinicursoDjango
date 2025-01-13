async function verificarDataValida() {
    const colaboradorId = document.getElementById('colaborador').value;
    const dataEscolhida = document.getElementById('data').value;

    if (!colaboradorId || !dataEscolhida) {
        return;
    }

    const dataLocal = new Date(dataEscolhida + 'T00:00:00-03:00');
    const diaSemana = dataLocal.getDay();

    const diasPermitidos = await fetchDiasPermitidos(colaboradorId);

    if (diasPermitidos.includes(diaSemana)) {
        fetchHorarios(colaboradorId, dataEscolhida);
    } else {
        alert('Este colaborador não está disponível nesta data.');
        const horaSelect = document.getElementById('hora');
        horaSelect.innerHTML = '<option value="" disabled selected>Selecione um horário</option>';
    }
}
