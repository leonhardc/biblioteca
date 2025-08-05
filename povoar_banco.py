import os
import django
from faker import Faker
import random
from django.contrib.auth.models import User
from usuario.models import Aluno, Professor, Funcionario
from usuario.constants import JORNADA
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


# TODO: Todas as funções já criadas até agora para povoar o banco de dados devem
# ser substituidas por versões mais simples e fáceis de entender. Por exemplo:
# 1. criar_usuario: deve criar um usuário no banco de dados e retornar esse 
# usuário para a função que o chamou.
# 2. criar_aluno: deve ser uma função que cria a entidade aluno no banco de dados
# 3. As funções criar_professor e criar_funcionario devem seguir a mesma lógica 
# aplicada nos itens 1 e 2.
# As funções de outras entidades do banco de dados devem seguir os mesmos aspectos
# relacionados a simplicidade.

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
    data['ativo'] = True
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
    data['ativo'] = True # FIX:Corrigir o warning dessa linha
    return data

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

def criar_funcionario():
    try:
        usuario = criar_usuario()
        if usuario:
            data = get_data_funcionario()
            professor = Professor.objects.create(usuario=usuario, **data) 
            return professor
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
def criar_n_alunos(n=1):
    for i in range(0,n):
        novo_aluno = criar_aluno()
        print(f'Aluno {novo_aluno.usuario.first_name} criado com sucesso.')













def criar_cursos():
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
        cod_curso = random.randint(1000, 9999)
        if not Curso.objects.filter(curso=curso).exists() or not Curso.objects.filter(cod_curso=cod_curso):
            try:
                novo_curso = Curso(
                    cod_curso = cod_curso,
                    curso = curso,
                    descricao = fake.paragraph(nb_sentences=5),
                    turno = random.choice(['M', 'V', 'I']),
                    duracao = random.choice([3, 4, 5])
                )
                novo_curso.save()
                print(f'Curso {curso} adicionado com sucesso.')
            except Exception as e:
                print(f'Erro ao adicionar {curso}.')

def criar_usuarios(alunos, professores, funcionarios):
    print('-'*20,'\nCriando Alunos ...')

    for _ in range(alunos):
        # Cria Usuário
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f'{first_name.lower()}{last_name.lower()}{random.randint(0, 999)}'
        email = f'{first_name.lower()}{last_name.lower()}@example.com'
        password = '123456'  # Pode mudar para algo mais seguro
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            print(f'Usuário {user.first_name} criado com sucesso!')
            # Criar Aluno
            print(f'Criando aluno {user.first_name} ...')
            try:
                matricula = f'{random.randint(100000, 999999)}'
                ids_cursos = list(Curso.objects.values_list('id', flat=True))
                curso = Curso.objects.get(id=random.choice(ids_cursos))
                endereco = fake.address().replace('\n', ', ')
                cpf = ''.join([str(random.randint(0,9)) for _ in range(11)])
                ingresso = datetime.date.today()
                conclusao = ingresso + relativedelta(years=+curso.duracao)
                novo_aluno = Aluno(
                    usuario = user, 
                    matricula = matricula,
                    curso = curso,
                    endereco = endereco,
                    cpf = cpf,
                    ingresso = ingresso,
                    conclusao_prevista = conclusao
                )
                novo_aluno.save()
                print('Novo aluno criado com sucesso.\n')
            except Exception as e:
                print(f'Erro ao criar aluno {user.first_name}\n')
                print(e)

    print('-'*20,'\nCriando Professores ...')

    for _ in range(professores):
        # Cria Usuário
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f'{first_name.lower()}{last_name.lower()}{random.randint(0, 999)}'
        email = f'{first_name.lower()}{last_name.lower()}@example.com'
        password = '123456'  # Pode mudar para algo mais seguro
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            print(f'Usuário {user.first_name} criado com sucesso!')
            # Criar Professor
            print(f'Criando professor {user.first_name} ...')
            try:
                matricula = f'{random.randint(1000, 9999)}'
                curso = random.choice(Curso.objects.all())
                cpf = ''.join([str(random.randint(0,9)) for _ in range(11)])
                regime = random.choice(['20', '40', 'DE'])
                novo_professor = Professor(
                    usuario = user, 
                    matricula = matricula,
                    curso = curso,
                    cpf = cpf,
                    regime = regime,
                )
                novo_professor.save()
                print('Novo professor criado com sucesso.\n')
            except Exception as e:
                print(f'Erro ao criar professor {user.first_name}\n')
    
    print('-'*20,'\nCriando Funcionarios ...')
    # Cria Usuário
    for _ in range(funcionarios):
        # Cria Usuário
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f'{first_name.lower()}{last_name.lower()}{random.randint(0, 999)}'
        email = f'{first_name.lower()}{last_name.lower()}@example.com'
        cpf = ''.join([str(random.randint(0,9)) for _ in range(11)])
        password = '123456'  # Pode mudar para algo mais seguro
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
            )
            print(f'Usuário {user.first_name} criado com sucesso!')
            # Criar Professor
            print(f'Criando Funcionário {user.first_name} ...')
            try:
                matricula = f'{random.randint(1000, 9999)}'
                novo_funcionario = Funcionario(
                    usuario = user, 
                    matricula = matricula, 
                    cpf = cpf
                )
                novo_funcionario.save()
                print('Novo funcionario criado com sucesso.')
            except Exception as e:
                print(f'Erro ao criar funcionario {user.first_name}')
    
    print('-'*20,'\nFim da execução.')


# Povoar banco de dados do app Livro 
def criar_autores(n_autores):
    for _ in range(n_autores):
        try:
            nome = fake.name()
            nacionalidade = random.choice(NACIONALIDADES)[0]
            cpf = ''.join([str(random.randint(0,9)) for _ in range(11)])
            novo_autor = Autor(
                nome = nome, 
                nacionalidade = nacionalidade,
                cpf = cpf
            )
            novo_autor.save()
            print('Novo autor adicionado com sucesso.\n')
        except Exception as e:
            print('Erro ao adicionar novo autor.')
            print(e)        


def criar_categorias():
    categorias = [
        'Calculo',
        'Fisica',
        'Quimica',
        'Programação',
        'Inteligencia Artificial',
        'Sistemas Operacionais',
        'Algebra Linear',
        'Anatomia',
        'Economia',
        'Sistemas Lineares',
    ]
    for categoria in categorias:
        try:
            nova_categoria = Categoria(
                categoria = categoria,
                descricao = fake.paragraph(nb_sentences=5)
            )
            nova_categoria.save()
            print('NOva categoria adicionada com sucesso')
        except Exception as e:
            print('Erro ao adicionar nova categoria.')
            print('Erro:',e)
        


def criar_livros(n_livros):
    for _ in range(n_livros):
        try:
            isbn = ''.join([str(random.randint(0,9)) for _ in range(6)])
            titulo = fake.sentence(nb_words=4)
            subtitulo = fake.sentence(nb_words=10)
            lancamento = gerar_data()
            editora = f'Editora: {fake.sentence(nb_words=2)}'
            copias = random.randint(10, 30)
            ids_autores = random.choices(list(Autor.objects.values_list('id', flat=True)), k=random.randint(1,3))
            autores = [Autor.objects.get(id=id) for id in ids_autores]
            ids_categorias = list(Categoria.objects.values_list('id', flat=True))
            categoria = Categoria.objects.get(id=int(random.choice(ids_categorias)))

            novo_livro = Livro.objects.create(
                isbn = isbn,
                titulo = titulo,
                subtitulo = subtitulo,
                lancamento = lancamento,
                editora = editora,
                copias = copias,
                categoria = categoria
            )
            novo_livro.autores.set(autores)
            novo_livro.save()

        except Exception as e:
            print('Erro ao adicionar novo livro.')
            print(e)


def corrigir_email():
    # Substitui o espaco que existe em alguns emails pelo caractere "_"
    usuarios = User.objects.all()
    for usuario in usuarios:
        usuario.email = f'{usuario.first_name.lower().replace(' ', '_')}{usuario.last_name.lower().replace(' ', '_')}@exemple.com'
        usuario.save()


def apagar_usuarios_vazios():
    # Apaga usuários que não são admins e que não estão associados a nenhum outro model.
    usuarios = User.objects.all()
    for usuario in usuarios:
        aluno = Aluno.objects.filter(usuario__username = usuario.username).exists()
        if aluno:
            continue
        professor = Professor.objects.filter(usuario__username = usuario.username).exists()
        if professor:
            continue
        funcionario = Funcionario.objects.filter(usuario__username = usuario.username).exists()
        if funcionario:
            continue
        if not usuario.is_superuser:
            usuario.delete()


if __name__ == '__main__':
    # TODO: Adicionar 100 alunos, 10 professores e 10 funcionarios.
    # criar_cursos()
    # criar_usuarios(100, 10, 10)
    corrigir_email()
    pass