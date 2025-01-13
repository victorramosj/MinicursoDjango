// Função para configurar a data mínima e desabilitar as datas não permitidas
async function configurarDataMinima() {
    const colaboradorId = document.getElementById('colaborador').value;
    const dataInput = document.getElementById('data');

    // Configura a data mínima como o dia de hoje
    const hoje = new Date();
    dataInput.min = hoje.toISOString().split('T')[0]; // Define o formato da data como YYYY-MM-DD

    // Desabilita as datas não permitidas (a lógica depende dos dias permitidos para o colaborador)
    if (colaboradorId) {
        const diasPermitidos = await fetchDiasPermitidos(colaboradorId);
        const todosDias = Array.from({ length: 7 }, (_, i) => i); // 0 - domingo, 1 - segunda-feira, ..., 6 - sábado

        // Função para comparar se a data é válida para o colaborador
        function isDataPermitida(data) {
            const diaSemana = data.getDay(); // Retorna o número do dia da semana (0 - domingo, 1 - segunda-feira, etc.)
            return diasPermitidos.includes(diaSemana);
        }

        // Verifica se a data escolhida é permitida
        dataInput.addEventListener('input', function () {
            const dataEscolhida = new Date(dataInput.value);
            if (!isDataPermitida(dataEscolhida)) {
                alert('Este colaborador não está disponível nesta data.');
                dataInput.value = ''; // Limpa a data se inválida
            }
        });
    }
}

// Função para buscar os dias permitidos para o colaborador
async function fetchDiasPermitidos(colaboradorId) {
    try {
        const response = await fetch(`/core/dias-permitidos/${colaboradorId}/`);
        const data = await response.json();
        return data.dias_permitidos;  // Retorna um array com os dias da semana permitidos
    } catch (error) {
        console.error('Erro ao buscar dias permitidos:', error);
    }
}

// Função para buscar horários disponíveis para o colaborador
async function fetchHorarios(colaboradorId, dataEscolhida) {
    try {
        const response = await fetch(`/core/horarios-disponiveis/${colaboradorId}/?data=${dataEscolhida}`);
        const data = await response.json();
        const horaSelect = document.getElementById('hora');
        horaSelect.innerHTML = '<option value="" disabled selected>Selecione um horário</option>';

        // Verifica se os horários existem
        if (data.horarios_disponiveis && data.horarios_disponiveis.length > 0) {
            // Usa Set para remover horários duplicados
            const horariosUnicos = [...new Set(data.horarios_disponiveis)];

            // Adiciona os horários únicos ao select
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

// Função para verificar se a data escolhida é válida
async function verificarDataValida() {
    const colaboradorId = document.getElementById('colaborador').value;
    const dataEscolhida = document.getElementById('data').value;

    if (!colaboradorId || !dataEscolhida) {
        return; // Não faz nada se o colaborador ou data não forem selecionados
    }

    // Ajusta a data para o fuso horário local (São Paulo)
    const dataLocal = new Date(dataEscolhida + 'T00:00:00-03:00'); // Força a data no fuso horário GMT-3
    const diaSemana = dataLocal.getDay(); // Retorna o número do dia da semana (0 - domingo, 1 - segunda-feira, etc.)

    // Busca os dias permitidos
    const diasPermitidos = await fetchDiasPermitidos(colaboradorId);

    // Verifica se o dia da semana é permitido
    if (diasPermitidos.includes(diaSemana)) {
        fetchHorarios(colaboradorId, dataEscolhida); // Data é enviada no formato ISO (YYYY-MM-DD)
    } else {
        alert('Este colaborador não está disponível nesta data.');
        const horaSelect = document.getElementById('hora');
        horaSelect.innerHTML = '<option value="" disabled selected>Selecione um horário</option>';
    }
}

// Função para configurar a data mínima e desabilitar as datas indisponíveis
async function configurarDataMinima() {
    const colaboradorId = document.getElementById('colaborador').value;
    const dataInput = document.getElementById('data');

    // Configura a data mínima como o dia de hoje
    const hoje = new Date();
    dataInput.min = hoje.toISOString().split('T')[0]; // Define o formato da data como YYYY-MM-DD

    // Desabilita as datas não permitidas (a lógica depende dos dias permitidos para o colaborador)
    if (colaboradorId) {
        const diasPermitidos = await fetchDiasPermitidos(colaboradorId);
        const todosDias = Array.from({ length: 7 }, (_, i) => i); // 0 - domingo, 1 - segunda-feira, ..., 6 - sábado

        // Desabilita as datas nos dias não permitidos
        const allDates = document.querySelectorAll('#data option');
        allDates.forEach((dateOption) => {
            const date = new Date(dateOption.value);
            if (!diasPermitidos.includes(date.getDay())) {
                dateOption.disabled = true;
            }
        });
    }
}
