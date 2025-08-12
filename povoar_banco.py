import os
import django
from faker import Faker
import random
from django.contrib.auth.models import User
from usuario.models import Aluno, Professor, Funcionario
from curso.models import Curso
from livro.models import Livro, Autor, Categoria, NACIONALIDADES
import datetime
from utils.utils import gerar_data
from dateutil.relativedelta import relativedelta
# from django.db.models import F

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')
django.setup()

fake = Faker('pt_BR') # Faz mapeamento de dados para nomes brasileiros.

# TODO: Testar as funções abaixo

# FUNÇÕES DO APP 'USUARIO'
# INICIO: Funções para gerar dados aleatorios
def gera_cpf_unico() -> str:
    cpf = ''
    while True:
        cpf = ''.join([str(random.randint(0,9)) for _ in range(11)])
        if not Aluno.objects.filter(cpf=cpf).exists():
            break
    return cpf

def gera_matricula_aluno() -> str:
    # Gera matricula de tamanho 6
    matricula = ''
    while True:
        matricula = f'{random.randint(100000, 999999)}'
        if not Aluno.objects.filter(matricula=matricula).exists():
            break
    return matricula

def gera_matricula_professor() -> str:
    # Gera matricula de tamanho 4 para professor
    matricula = ''
    while True:
        matricula = f'{random.randint(1000, 9999)}'
        if not Professor.objects.filter(matricula=matricula).exists():
            break
    return matricula

def gerar_matricula_funcionario() -> str:
    # Gera matricula de tamanho 4 para funcionario
    matricula = ''
    while True:
        matricula = f'{random.randint(1000, 9999)}'
        if not Funcionario.objects.filter(matricula=matricula).exists():
            break
    return matricula

# INICIO: Funções para gerações de dados para as entidades do banco de dados
def get_data_usuario() -> dict[str, str]:
    data: dict[str, str] = { 
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "password": "1234", # Senha padrão
    }
    data['username'] = f'{str(data['first_name']).lower()}{str(data["last_name"]).lower()}{random.randint(0, 999)}'
    data['email'] = f'{str(data["first_name"]).lower()}{str(data['last_name']).lower()}@example.com'
    return data

def get_data_aluno() -> dict[str, str|datetime.datetime|datetime.date|Curso]:
    ids_cursos = list(Curso.objects.values_list('id', flat=True))
    curso = Curso.objects.get(id=random.choice(ids_cursos))
    data:dict[str, str|datetime.datetime|datetime.date|Curso] = {}
    data['matricula'] = gera_matricula_aluno()
    data['curso'] = curso
    data['cpf'] = gera_cpf_unico()
    data['endereco'] = fake.address().replace('\n', ', ')
    data['ingresso'] = datetime.date.today()
    data['conclusao'] = data['ingresso'] + relativedelta(years=+curso.duracao) # type: ignore
    data['ativo'] = True # type: ignore
    return data

def get_data_professor() -> dict[str, str|datetime.datetime|datetime.date|Curso|bool]: 
    data:dict[str, str|datetime.datetime|datetime.date|Curso] = {}
    ids_cursos = list(Curso.objects.values_list('id', flat=True))
    curso = Curso.objects.get(id=random.choice(ids_cursos))
    data['matricula'] = gera_matricula_professor()
    data['curso'] = curso
    data['cpf'] = gera_cpf_unico()
    data['regime'] = random.choice(['20', '40', 'DE']) # TODO:Mudar essa linha para receber os elementos de JORNADA
    data['contratacao'] = datetime.date.today()
    data['ativo'] = True # type: ignore # FIX:Corrigir o warning dessa linha
    return data # type: ignore

def get_data_funcionario() -> dict[str, str|datetime.datetime|datetime.date|Curso|bool]:
    data:dict[str, str|datetime.datetime|datetime.date|Curso|bool] = {}
    data['matricula'] = gerar_matricula_funcionario()
    data['cpf'] = gera_cpf_unico()
    data['ativo'] = True
    return data

# INICIO: Criação das entidades do banco de dados
def criar_usuario() -> User|None:
    data = get_data_usuario()
    if User.objects.filter(username=data['username']).exists():
        raise Exception("O usuário já existe na base de dados.")
    user = User.objects.create_user(**data)
    if not user:
        raise Exception("Erro ao salvar o usuário na base de dados.")
    return user

def criar_aluno() -> Aluno|None:
    try:
        usuario = criar_usuario()
        if usuario:
            data = get_data_aluno()
            aluno = Aluno.objects.create(usuario=usuario,**data)
            return aluno
    except Exception as e:
        print(e)
        return None

def criar_professor() -> Professor|None:
    try:
        usuario = criar_usuario()
        if usuario:
            data = get_data_professor()
            professor = Professor.objects.create(usuario=usuario,**data)
            return professor
    except Exception as e:
        print(e)
        return None

def criar_funcionario() -> Funcionario|None:
    try:
        usuario = criar_usuario()
        if usuario:
            data = get_data_funcionario()
            funcionario = Funcionario.objects.create(usuario=usuario, **data) 
            return funcionario
    except Exception as e:
        print(e)
        return None

# FUNÇÕES DO APP LIVROS
def gerar_isbn_unico() -> str:
    # Gera isbn unico na base de dados
    isbn = ''
    while True:
        isbn = f'{random.randint(100000, 999999)}'
        if not Livro.objects.filter(isbn=isbn).exists():
            break
    return isbn

def get_data_autor() -> dict[str, str]:
    data:dict[str, str] = {}
    data['nome'] = fake.name()
    data['nacionalidade'] = random.choice(NACIONALIDADES)[0]
    data['cpf'] = ''.join([str(random.randint(0,9)) for _ in range(11)])
    return data

def get_data_livro() -> dict[str, str|int|Categoria|list[Autor]|Categoria|datetime.date]:
    data:dict[str, str|int|Categoria|list[Autor]|Categoria|datetime.date] = {}
    ids_autores = random.choices(list(Autor.objects.values_list('id', flat=True)), k=random.randint(1,3))
    ids_categorias = list(Categoria.objects.values_list('id', flat=True))
    data['isbn'] = gerar_isbn_unico()
    data['titulo'] = fake.sentence(nb_words=4)
    data['subtitulo'] = fake.sentence(nb_words=10)
    data['lancamento'] = gerar_data()
    data['editora'] = f'Editora {fake.sentence(nb_words=2)}'
    data['copias'] = random.randint(10, 30)
    data['autores'] = [Autor.objects.get(id=id) for id in ids_autores]
    data['categoria'] = Categoria.objects.get(id=int(random.choice(ids_categorias)))
    return data

def criar_autor() -> Autor:
    # Cria um autor na base de dados
    data = get_data_autor()
    autor = Autor.objects.create(**data)
    return autor

def criar_categoria(categoria:str, desc_categoria:str) -> Categoria:
    # Cria uma categoria no banco de dados usando categoria como nome da categoria
    # de livros e desc_categoria como a descrição
    nova_categoria = Categoria.objects.create(categoria=categoria, descricao=desc_categoria)
    return nova_categoria

def criar_livro() -> Livro:
    # Cria um livro na base de dados
    data = get_data_livro()
    livro = Livro.objects.create(**data)
    return livro

# 'reservas' e 'emprestimos' não serão criados por padrão

# FUNÇÕES DO APP CURSO
def criar_curso(cod_curso:str, curso:str, descricao:str, turno:str, duracao:int) -> Curso:
    novo_curso = Curso.objects.create(
        cod_curso=cod_curso,
        curso=curso,
        descricao=descricao,
        turno=turno,
        duracao=duracao
    )
    return novo_curso

# Funções para criar vários componentes no banco de dados
def criar_n_alunos(n_alunos:int=1):
    for _ in range(0,n_alunos):
        novo_aluno = criar_aluno()
        print(f'Aluno {novo_aluno.matricula}:{novo_aluno.usuario} criado com sucesso.') # type: ignore

def criar_n_professores(n_professores:int=1):
    for _ in range(0, n_professores):
        novo_professor = criar_professor()
        print(f'Professor {novo_professor.matricula}:{novo_professor.usuario} criado com sucesso.') # type: ignore

def criar_n_funcionarios(n_funcionarios:int=1):
    for _ in range(0, n_funcionarios):
        novo_funcionario = criar_funcionario()
        print(f'Funcionario {novo_funcionario.matricula}:{novo_funcionario.usuario} criado com sucesso.') # type: ignore

def criar_n_livros(n_livros:int=1):
    for _ in range(0, n_livros):
        novo_livro = criar_livro()
        print(f"Livro {novo_livro.isbn}: {novo_livro.titulo} criado com sucesso.") # type: ignore

def criar_n_autores(n_autores:int=1):
    for _ in range(0, n_autores):
        novo_autor = criar_autor()
        print(f"Autor {novo_autor.id}: {novo_autor.nome} criado com sucesso.") # type: ignore

def criar_categorias(categorias:list[str]):
    for categoria in categorias:
        desc_categoria = fake.sentence(nb_words=10)
        nova_categoria = criar_categoria(categoria, desc_categoria)
        print(f"Categoria {nova_categoria.id}: {nova_categoria.categoria} criada com sucesso.") # type: ignore

def criar_n_cursos(dict_cursos:list[dict[str,str|int]]):
    lista_de_cursos = [
        'Engenharia de Computação',
        'Engenharia Eletrica',
        'Musica',
        'Economia',
        'Odontologia',
        'Medicina',
        'Enfermagem',        
    ]
    for curso in lista_de_cursos:
        curso_dict:dict[str, str|int] = {
            "cod_curso": f'{random.randint(1000, 9999)}',
            "curso": curso,
            "descricao": fake.sentence(nb_words=20),
            "turno": random.choice(['M', 'V', 'I']),
            'duracao': random.choice([3, 4, 5])
        }
        novo_curso = criar_curso(**curso_dict) # type: ignore
        print(f'{novo_curso.cod_curso} - {novo_curso.curso} criado com sucesso.') # type: ignore


if __name__ == '__main__':
    pass