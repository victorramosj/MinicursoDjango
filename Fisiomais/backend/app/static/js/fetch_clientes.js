async function fetchClientes() {
    try {
        const response = await fetch('/usuarios/clientes/');
        const data = await response.json();
        const clienteSelect = document.getElementById('cliente');
        clienteSelect.innerHTML = '<option value="" disabled selected>Selecione um cliente</option>';
        data.clientes.forEach(cliente => {
            const option = document.createElement('option');
            option.value = cliente.id;
            option.textContent = cliente.nome;
            clienteSelect.appendChild(option);
        });
    } catch (error) {
        console.error('Erro ao buscar clientes:', error);
    }
}

fetchClientes();
