import os
import django
from faker import Faker
import random
from django.contrib.auth.models import User
from usuario.models import Aluno, Professor, Funcionario
from curso.models import Curso
import datetime
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
    print('Criando Alunos ...')
    
    for _ in range(alunos):
        # Cria Usuário
        username = fake.user_name()
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
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
                curso = random.choice(Curso.objects.all())
                endereco = fake.address().replace('\n', ', ')
                cpf = random.randint(100000000000, 99999999999)
                ingresso = datetime.date.today()
                conclusao = ingresso + relativedelta(years=+5)
                novo_aluno = Aluno(
                    usuario = user, 
                    matricula = matricula,
                    curso = curso,
                    endereco = endereco,
                    cpf = cpf,
                    ingresso = ingresso,
                    conclusao = conclusao
                )
                novo_aluno.save()
                print('Novo aluno criado com sucesso.')
            except Exception as e:
                print(f'Erro ao criar aluno {user.first_name}')

    print('Criando Professores ...')
    # TODO: Implementar a inserção de professores
    print('Criando Funcionarios ...')
    # TODO: Implementar a inserção de funcionários

if __name__ == '__main__':
    # TODO: Adicionar 100 alunos, 10 professores e 10 funcionarios.
    pass