// Evento assim que a página é carregada
window.addEventListener('load', 
    function() {
        if(window.location.search.includes('professor')){
            document.getElementById('aba-professores').click()
        }
        if(window.location.search.includes('funcionario')){
            document.getElementById('aba-funcionarios').click()
        }
        if(window.location.search.includes('autor')){
            document.getElementById('aba-autores').click()
        }
        if(window.location.search.includes('categoria')){
            document.getElementById('aba-categorias').click()
        }
        if(window.location.search.includes('reserva')){
            document.getElementById('aba-reservas').click()
        }
        if(window.location.search.includes('emprestimo')){
            document.getElementById('aba-emprestimos').click()
        }
    }
)
// Usuários
if(window.location.pathname === '/administrador/usuarios/'){
    console.log('Entrou!')
    document.getElementById('aba-alunos').addEventListener('click',(event)=>{openTab(event,'conteudo-aba-alunos')})
    document.getElementById('aba-professores').addEventListener('click',(event)=>{openTab(event,'conteudo-aba-professores')})
    document.getElementById('aba-funcionarios').addEventListener('click',(event)=>{openTab(event,'conteudo-aba-funcionarios')})
}
// Livros
if(window.location.pathname === '/administrador/livros/'){
    document.getElementById('aba-livros').addEventListener('click', (event)=> {openTab(event, 'conteudo-aba-livros')})
    document.getElementById('aba-autores').addEventListener('click', (event)=> {openTab(event, 'conteudo-aba-autores')})
    document.getElementById('aba-categorias').addEventListener('click', (event)=> {openTab(event, 'conteudo-aba-categorias')})
    document.getElementById('aba-reservas').addEventListener('click', (event)=> {openTab(event, 'conteudo-aba-reservas')})
    document.getElementById('aba-emprestimos').addEventListener('click', (event)=> {openTab(event, 'conteudo-aba-emprestimos')})
}
// Cursos
if(window.location.pathname === '/administrador/cursos/'){}

function openTab(event, tabId) {
    // Esconde todos os conteúdos das abas
    let tabContents = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = "none";
    }
    // Remove a classe 'tab-ativa' de todos os botões
    let tabButtons = document.getElementsByClassName("tab-button");
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove("tab-ativa");
    }
    // Mostra o conteúdo da aba selecionada
    document.getElementById(tabId).style.display = "block";
    // Adiciona a classe 'active' ao botão da aba atual
    event.currentTarget.classList.add("tab-ativa");
    // Muda o valor de href do botão de adicionar aluno, professor ou funcionario
    let botaoAddUsuario = document.getElementById('botao-add-usuario');
    let botaoAddLivro = document.getElementById('botao-add-livro');
    if (event.currentTarget.id === 'aba-alunos'){
        botaoAddUsuario.href = `${window.location.origin}/administrador/criar-aluno/`
    }
    if (event.currentTarget.id === 'aba-professores'){
        botaoAddUsuario.href = `${window.location.origin}/administrador/criar-professor/`
    }
    if (event.currentTarget.id === 'aba-funcionarios'){
        botaoAddUsuario.href = `${window.location.origin}/administrador/criar-funcionario/`
    }
    if (event.currentTarget.id === 'aba-livros'){
        botaoAddLivro.href = `${window.location.origin}/livro/criar-livro/`
    }
    if (event.currentTarget.id === 'aba-autores'){
        botaoAddLivro.href = `${window.location.origin}/livro/criar-autor/`
    }
    if (event.currentTarget.id === 'aba-categorias'){
        botaoAddLivro.href = `${window.location.origin}/livro/criar-categoria/`
    }
    if (event.currentTarget.id === 'aba-reservas'){
        botaoAddLivro.href = `${window.location.origin}/livro/criar-reserva/`
    }
    if (event.currentTarget.id === 'aba-emprestimos'){
        botaoAddLivro.href = `${window.location.origin}/livro/criar-emprestimo/`
    }
}

// Evento para exibir o campo de pesquisa
const iconePesqusar = document.querySelector('.icone-pesquisa')
if (iconePesqusar){
    iconePesqusar.addEventListener('click', function(event) {
        event.currentTarget.style.display = "none"
        document.querySelector('.form-pesquisa').style.display = "block"
    })
}

const iconeFechar =  document.querySelector('.icone-fechar')
if (iconeFechar) {
    iconeFechar.addEventListener('click', function() {
        document.querySelector('.icone-fechar').parentElement.style.display = "none"
    })
}