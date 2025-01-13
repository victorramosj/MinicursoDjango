async function fetchDiasPermitidos(colaboradorId) {
    try {
        const response = await fetch(`/core/dias-permitidos/${colaboradorId}/`);
        const data = await response.json();
        return data.dias_permitidos;  // Retorna um array com os dias da semana permitidos
    } catch (error) {
        console.error('Erro ao buscar dias permitidos:', error);
    }
}
