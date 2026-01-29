        // Função de pesquisa de usuário (a ser implementada)
        document.getElementById('usuario-pesquisar').addEventListener('keyup', function() {
            const query = this.value.toLowerCase();
            const select = document.getElementById('id_usuario');
            const dataList = document.getElementById('usuario-list');
            dataList.innerHTML = '';
            for (let i = 0; i < select.options.length; i++) {
                const option = select.options[i];
                if (option.text.toLowerCase().includes(query)) {
                    const dataOption = document.createElement('option');
                    dataOption.value = option.text;
                    dataList.appendChild(dataOption);
                    option.style.display = '';
                } else {
                    option.style.display = 'none';
                }
            }
        });
        document.getElementById('usuario-pesquisar').addEventListener('change', function() {
            const value = this.value;
            const select = document.getElementById('id_usuario');
            for (let i = 0; i < select.options.length; i++) {
                const option = select.options[i];
                if (option.text === value) {
                    select.value = option.value;
                    break;
                }
            }
        });