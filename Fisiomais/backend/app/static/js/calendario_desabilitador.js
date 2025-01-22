document.addEventListener("DOMContentLoaded", function () {
    const colaboradorSelect = document.getElementById("colaborador");
    const dataInput = document.getElementById("data");
    const horaSelect = document.getElementById("hora");
    let diasPermitidos = [];
    let feriados = [];

    // Função para calcular os feriados
    function calcularFeriados() {
        const ano = new Date().getFullYear();
        feriados = [
            `${ano}-01-01`, // Ano Novo
            `${ano}-03-01`, // Carnaval (ajustar se necessário)
            `${ano}-03-02`,
            `${ano}-03-03`,
            `${ano}-03-04`,
            `${ano}-04-21`, // Tiradentes
            `${ano}-05-01`, // Dia do Trabalhador
            `${ano}-06-08`, // Corpus Christi (ajustar se necessário)
            `${ano}-09-07`, // Independência
            `${ano}-10-12`, // Nossa Senhora Aparecida
            `${ano}-11-02`, // Finados
            `${ano}-11-15`, // Proclamação da República
            `${ano}-12-24`, // Véspera de Natal
            `${ano}-12-25`  // Natal
        ];
    }

    calcularFeriados();

    // Inicializar o calendário com Flatpickr
    const calendario = flatpickr(dataInput, {
        dateFormat: "Y-m-d", // Formato enviado ao backend
        locale: "pt", // Idioma para português
        disable: [
            function (date) {
                const dataFormatada = date.toISOString().split("T")[0]; // Data sem ajuste de fuso horário

                if (diasPermitidos.length === 0) {
                    return true; // Desabilita todos os dias se nenhum permitido
                }

                const isDisabled = !diasPermitidos.includes(date.getDay()) || feriados.includes(dataFormatada);
                return isDisabled;
            }
        ],
        minDate: "today", // Apenas datas a partir de hoje
        onChange: function (selectedDates) {
            if (selectedDates.length > 0) {
                const diaSelecionado = selectedDates[0]; // Sem ajustes de fuso
                const dataFormatada = diaSelecionado.toISOString().split("T")[0];
                dataInput.value = dataFormatada; // Define a data no formato do backend
                
                const colaboradorId = colaboradorSelect.value;
                if (colaboradorId) {
                    // Chama a função fetchHorarios para buscar os horários disponíveis
                    fetchHorarios(colaboradorId, dataFormatada);
                }
            }
        }
    });

    // Atualizar dias permitidos ao selecionar um colaborador
    colaboradorSelect.addEventListener("change", async function () {
        const colaboradorId = colaboradorSelect.value;

        if (colaboradorId) {
            try {
                const response = await fetch(`/core/dias-permitidos/${colaboradorId}/`);
                const data = await response.json();
                diasPermitidos = data.dias_permitidos || [];

                // Atualizar o calendário com os novos dias permitidos
                calendario.set("disable", [
                    function (date) {
                        const dataFormatada = date.toISOString().split("T")[0];
                        return !diasPermitidos.includes(date.getDay()) || feriados.includes(dataFormatada);
                    }
                ]);

                // Atualiza os horários para o colaborador selecionado, se houver data selecionada
                const dataEscolhida = dataInput.value;
                if (dataEscolhida) {
                    fetchHorarios(colaboradorId, dataEscolhida);
                }
            } catch (error) {
                console.error("Erro ao buscar dias permitidos:", error);
                alert("Não foi possível carregar os dias permitidos.");
            }
        }
    });
});
