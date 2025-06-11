from datetime import date
from livro.models import Livro, Autor, Categoria, Reserva, Emprestimo
from usuario.models import Aluno, Professor, Funcionario
from curso.models import Curso

def informacoes_formulario_aluno(aluno:Aluno, endereco:dict[str,str]):
    data:dict[str, str|date] = {}
    data = {
        'nome' : aluno.usuario.first_name,              # type: ignore
        'sobrenome' : aluno.usuario.last_name,          # type: ignore
        'email' : aluno.usuario.email,                  # type: ignore
        'usuario' : aluno.usuario.username,             # type: ignore
        'tipo_logradouro' : endereco['tipo_logradouro'],
        'logradouro' : endereco['logradouro'],
        'numero' : endereco['numero'],
        'bairro' : endereco['bairro'],
        'cidade' : endereco['cidade'],
        'estado' : endereco['estado'],
        'cep' : endereco['cep'],
        'complemento' : endereco['complemento'],
        'matricula' : aluno.matricula,                  # type: ignore
        'cpf' : aluno.cpf,                              # type: ignore
        'curso' : aluno.curso.cod_curso,                # type: ignore
        'ingresso' : aluno.ingresso,                    # type: ignore
        'conclusao_prevista' : aluno.conclusao_prevista # type: ignore
    }
    return data

def informacoes_formulario_professor(professor:Professor):
    data:dict[str, str|date] = {}
    data = {
        'nome': professor.usuario.first_name,           # type: ignore
        'sobrenome': professor.usuario.last_name,       # type: ignore
        'email': professor.usuario.email,               # type: ignore
        'usuario': professor.usuario.username,          # type: ignore
        'matricula': professor.matricula,               # type: ignore
        'curso': professor.curso.cod_curso,             # type: ignore
        'cpf': professor.cpf,                           # type: ignore
        'regime': professor.regime,                     # type: ignore
        'contratacao': professor.contratacao            # type: ignore
    }
    return data

def informacoes_formulario_funcionario(funcionario:Funcionario):
    data:dict[str, str] = {
        'nome': funcionario.usuario.first_name,         # type: ignore
        'sobrenome': funcionario.usuario.last_name,     # type: ignore
        'email': funcionario.usuario.email,             # type: ignore
        'usuario': funcionario.usuario.username,        # type: ignore
        'matricula': funcionario.matricula,             # type: ignore
        'cpf': funcionario.cpf                          # type: ignore
    }
    return data

def informacoes_formulario_livro(livro:Livro):
    data:dict[str, str|list[int]|int|date] = {}
    data = {
        'isbn': livro.isbn,                                     # type: ignore
        'titulo': livro.titulo,                                 # type: ignore
        'subtitulo': livro.subtitulo,                           # type: ignore
        'lancamento': livro.lancamento,                         # type: ignore
        'editora': livro.editora,                               # type: ignore
        'copias': livro.copias,                                 # type: ignore
        'autores': [autor.id for autor in livro.autores.all()], # type: ignore
        'categoria': livro.categoria.id                         # type: ignore
    }
    return data

def informacoes_formulario_autor(autor:Autor):
    data:dict[str, str] = {
        'nome': autor.nome,                                     # type: ignore
        'cpf': autor.cpf,                                       # type: ignore
        'nacionalidade': autor.nacionalidade                    # type: ignore
    }
    return data

def informacoes_formulario_categoria(categoria:Categoria):
    data:dict[str, str] = {
        'categoria': categoria.categoria,                       # type: ignore
        'descricao': categoria.descricao                        # type: ignore
    }
    return data

def informacoes_formulario_reserva(reserva:Reserva):
    data:dict[str, str|date] = {
        'usuario': reserva.usuario.username,                    # type: ignore
        'livro': reserva.livro.isbn,                            # type: ignore
        'data_reserva': reserva.data_reserva                    # type: ignore
    }
    return data

def informacoes_formulario_emprestimo(emprestimo:Emprestimo):
    data:dict[str, str|date] = {
        'usuario': emprestimo.usuario.id,                          # type: ignore
        'livro': emprestimo.livro.id,                              # type: ignore
        'data_emprestimo': emprestimo.data_emprestimo.strftime("%Y-%m-%d"),          # type: ignore
        'data_devolucao': emprestimo.data_devolucao.strftime("%Y-%m-%d")             # type: ignore
    }
    return data

def informacoes_formulario_curso(curso:Curso):
    data:dict[str, str] = {
        'cod_curso': curso.cod_curso,                           # type: ignore
        'curso': curso.curso,                                   # type: ignore
        'descricao': curso.descricao,                           # type: ignore
        'turno': curso.turno,                                   # type: ignore
        'duracao': curso.duracao,                               # type: ignore
    }
    return data