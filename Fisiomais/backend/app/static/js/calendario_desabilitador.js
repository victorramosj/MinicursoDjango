document.addEventListener("DOMContentLoaded", function () {
    const colaboradorSelect = document.getElementById("colaborador");
    const dataInput = document.getElementById("data");
    let diasPermitidos = [];
    let feriados = [];

    // Função para calcular os feriados
    function calcularFeriados() {
        const ano = new Date().getFullYear();
        feriados = [
            `${ano}-01-01`, // Ano Novo
            `${ano}-04-01`, // Carnaval (ajustar se necessário)
            `${ano}-03-02`,
            `${ano}-03-03`,
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

                // Verifica se a data está disponível ou não
                console.log("Verificando data:", dataFormatada);
                console.log("Dias permitidos:", diasPermitidos);
                

                if (diasPermitidos.length === 0) {
                    console.log("Nenhum dia permitido configurado.");
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

                // Formatar a data no formato brasileiro para exibição
                const dataFormatadaBR = diaSelecionado.toLocaleDateString("pt-BR", {
                    day: "2-digit",
                    month: "2-digit",
                    year: "numeric"
                });

                console.log("Data selecionada:", dataFormatadaBR);
                dataInput.value = dataFormatadaBR; // Exibe a data no formato brasileiro
            }
        }
    });

    // Atualizar dias permitidos ao selecionar um colaborador
    colaboradorSelect.addEventListener("change", async function () {
        const colaboradorId = colaboradorSelect.value;
        console.log("Colaborador selecionado:", colaboradorId);

        if (colaboradorId) {
            try {
                const response = await fetch(`/core/dias-permitidos/${colaboradorId}/`);
                const data = await response.json();
                diasPermitidos = data.dias_permitidos || [];

                console.log("Dias permitidos recebidos:", diasPermitidos);

                // Atualizar o calendário com os novos dias permitidos e feriados
                calendario.set("disable", [
                    function (date) {
                        const dataFormatada = date.toISOString().split("T")[0]; // Data sem ajuste de fuso horário
                        console.log("Verificando novamente a data:", dataFormatada);

                        const isDisabled = !diasPermitidos.includes(date.getDay()) || feriados.includes(dataFormatada);
                        console.log(`Dia ${dataFormatada} está ${isDisabled ? "desabilitado" : "habilitado"}`);
                        return isDisabled;
                    }
                ]);
            } catch (error) {
                console.error("Erro ao buscar dias permitidos:", error);
                alert("Não foi possível carregar os dias permitidos.");
            }
        }
    });
});
