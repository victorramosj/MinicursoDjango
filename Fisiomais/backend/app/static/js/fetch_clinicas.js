async function fetchClinicas() {
    try {
        const response = await fetch('/usuarios/clinicas/');
        const data = await response.json();
        const clinicaSelect = document.getElementById('clinica');
        clinicaSelect.innerHTML = '<option value="" disabled selected>Selecione uma clínica</option>';
        data.clinicas.forEach(clinica => {
            const option = document.createElement('option');
            option.value = clinica.id;
            option.textContent = clinica.nome;
            clinicaSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Erro ao buscar clínicas:', error);
    }
}
