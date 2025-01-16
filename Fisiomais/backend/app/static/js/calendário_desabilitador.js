document.addEventListener("DOMContentLoaded", async () => {
    const colaboradorSelect = document.getElementById("colaborador");
    const dataInput = document.getElementById("data");

    if (colaboradorSelect) {
        colaboradorSelect.addEventListener("change", async function () {
            const colaboradorId = this.value;

            if (colaboradorId) {
                try {
                    // Faz a chamada para obter os dias permitidos
                    const response = await fetch(`/core/dias-permitidos/${colaboradorId}/`);
                    if (!response.ok) {
                        throw new Error("Erro ao buscar dias permitidos.");
                    }

                    const data = await response.json();
                    const diasPermitidos = data.dias_permitidos; // Exemplo: ["segunda-feira", "quarta-feira", "sexta-feira"]

                    // Converte os dias da semana para índices numéricos (0 = domingo, 6 = sábado)
                    const diasPermitidosIndices = diasPermitidos.map(dia => {
                        const diaSemana = {
                            "domingo": 0,
                            "segunda-feira": 1,
                            "terça-feira": 2,
                            "quarta-feira": 3,
                            "quinta-feira": 4,
                            "sexta-feira": 5,
                            "sábado": 6,
                        };
                        return diaSemana[dia];
                    });

                    // Atualiza o calendário desabilitando os dias não permitidos
                    dataInput.addEventListener("input", function () {
                        const dataSelecionada = new Date(this.value);
                        const diaSemana = dataSelecionada.getDay();

                        if (!diasPermitidosIndices.includes(diaSemana)) {
                            alert("Este dia da semana não está disponível para o colaborador.");
                            this.value = ""; // Limpa a data inválida
                        }
                    });

                    // Define um atributo para bloquear manualmente os dias
                    dataInput.disabled = false;
                } catch (error) {
                    console.error(error);
                    alert("Erro ao carregar os dias disponíveis do colaborador.");
                    dataInput.disabled = true;
                }
            }
        });
    }
});
