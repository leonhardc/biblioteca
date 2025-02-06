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

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seu_projeto.settings')
django.setup()

fake = Faker('pt_BR') # Faz mapeamento de dados para nomes brasileiros.

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
                    matricula = matricula
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
            novo_autor = Autor(
                nome = nome, 
                nacionalidade = nacionalidade
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

if __name__ == '__main__':
    # TODO: Adicionar 100 alunos, 10 professores e 10 funcionarios.
    criar_cursos()
    criar_usuarios(100, 10, 10)
    pass