document.getElementById('servico').addEventListener('change', function() {
    const servicoId = this.value;
    const clinicaId = document.getElementById('clinica').value;
    if (servicoId && clinicaId) {
        fetchColaboradores(servicoId, clinicaId);
    }
});

document.getElementById('clinica').addEventListener('change', function() {
    const servicoId = document.getElementById('servico').value;
    const clinicaId = this.value;
    if (servicoId && clinicaId) {
        fetchColaboradores(servicoId, clinicaId);
    }
});

document.getElementById('colaborador').addEventListener('change', function() {
    const colaboradorId = this.value;
    const dataEscolhida = document.getElementById('data').value;
    if (colaboradorId && dataEscolhida) {
        verificarDataValida();
    }
});

document.getElementById('data').addEventListener('change', function() {
    const colaboradorId = document.getElementById('colaborador').value;
    const dataEscolhida = this.value;
    if (colaboradorId && dataEscolhida) {
        verificarDataValida();
    }
});

// Chama a função de planos quando o serviço for selecionado
document.getElementById('servico').addEventListener('change', function() {
    const servicoId = this.value;
    if (servicoId) {
        fetchPlanos(servicoId); // Busca os planos para o serviço selecionado
    }
});

