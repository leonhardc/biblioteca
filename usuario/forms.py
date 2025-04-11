from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from usuario.models import Aluno
from curso.models import Curso
from django.core.exceptions import ValidationError
import re

ESTADOS_BRASIL = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espirito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MS', 'Mato Grosso do Sul'),
    ('MT', 'Mato Grosso'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
)
OPCOES_CURSOS = tuple([(e.cod_curso, f'{e.cod_curso} - {e.curso}') for e in Curso.objects.all()])
JORNADA = (
        ('20', '20hr'),
        ('40', '40hr'),
        ('DE', 'Dedicação Exclusiva'),
    )

class LoginForm(forms.Form):
    usuario = forms.CharField(label='Usuário', max_length=255, 
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usuário', 'style': 'background-color:#e5ebf4'}))
    senha = forms.CharField(label='Senha', max_length=255, 
                            widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Senha', 'style': 'background-color:#e5ebf4'}))

class FormularioAluno(forms.Form):
    # Dados Pessoais
    nome = forms.CharField(label='Nome', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite o nome do aluno'}))
    sobrenome = forms.CharField(label='Sobrenome', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite o sobrenome do aluno'}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email do aluno'}))
    usuario = forms.CharField(label='Usuário', max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite seu nome de usuário'}))
    # Endereço
    rua = forms.CharField(label='Rua', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite o nome da rua'}))
    numero = forms.CharField(label='Numero',max_length=6,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite o numero da casa'}))
    bairro = forms.CharField(label='Bairro',max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite o nome do bairro'}))
    cidade = forms.CharField(label='Cidade',max_length=50,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite o nome da cidade'}))
    estado = forms.ChoiceField(label='Estado',choices=ESTADOS_BRASIL, widget=forms.Select(attrs={'class':'form-control'}))
    cep = forms.CharField(label='CEP',max_length=8,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite o CEP'}))
    complemento = forms.CharField(label='Complemento',max_length=200,widget=forms.TextInput(attrs={'class':'form-control' , 'placeholder':''}))
    # Curso
    matricula = forms.CharField(label='Matricula', max_length=6,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite a matricula do aluno'}))
    curso = forms.ChoiceField(label='Curso',choices=OPCOES_CURSOS, widget=forms.Select(attrs={'class':'form-control'}))
    ingresso = forms.DateField(label="Data de Ingresso")
    conclusao_prevista = forms.DateField(label="Data de Conclusão")
    
    def clean_senha_confirmacao(self):
        senha = self.cleaned_data['senha']
        senha_confirmacao = self.cleaned_data['senha_confirmacao']
        if senha != senha_confirmacao:
            raise ValidationError('As senhas digitadas não são iguais.')
        return senha_confirmacao
    
    def clean_nome(self):
        nome = self.cleaned_data['nome']
        if re.search(r'[0-9]', nome):
            raise ValidationError('O nome do aluno não pode conter números.')
        return nome

    def clean_sobrenome(self):
        sobrenome = self.cleaned_data['sobrenome']
        if re.search(r'[0-9]', sobrenome):
            raise ValidationError('O sobrenome do aluno não pode conter números.')
        return sobrenome

    def clean_email(self):
        formato_email = r'^[a-zA-Z0-9.-_]+@[a-zA-Z0-9]+\.[a-zA-Z\.a-zA-Z]{1,3}'
        email = self.cleaned_data['email']
        if not re.match(formato_email, email):
            raise ValidationError('Formato inválido.')
        return email
                    

    def clean_matricula(self):
        matricula = self.cleaned_data['matricula']
        if re.search(r'[a-zA-Z]', matricula):
            raise ValidationError('O campo de matricula deve conter somente numeros.')
        return matricula

    def clean_cep(self):
        cep = self.cleaned_data['cep']
        if len(cep) != 8:
            raise ValidationError('O CEP deve conter 8 caracteres.') 
        if re.match(r'[a-zA-Z]', cep):
            raise ValidationError('O campo CEP não deve conter letras.')

class FormularioProfessor(forms.Form):
    nome = forms.CharField(label='Nome', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite o nome do aluno'}))
    sobrenome = forms.CharField(label='Sobrenome', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite o sobrenome do aluno'}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email do aluno'}))
    usuario = forms.CharField(label='Usuário', max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite seu nome de usuário'}))
    matricula = forms.CharField(label='Matricula', max_length=4, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Matricula do professor'}))
    curso = forms.ChoiceField(label='Curso',choices=OPCOES_CURSOS, widget=forms.Select(attrs={'class':'form-control'}))
    cpf = forms.CharField(label='CPF', widget=forms.TextInput(attrs={'class':'form-control'}))
    regime = forms.ChoiceField(label='Regime', choices=JORNADA, widget=forms.Select(attrs={'class':'form-control'}))
    contratacao = forms.DateField(label='Contratação', widget=forms.DateInput(attrs={'type':'date'}))
    # TODO: Implementar os metodos _clean dos atributos do formulário

class FormularioFuncionario(forms.Form):
    nome = forms.CharField(label='Nome', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite o nome do aluno'}))
    sobrenome = forms.CharField(label='Sobrenome', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite o sobrenome do aluno'}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email do aluno'}))
    usuario = forms.CharField(label='Usuário', max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Digite seu nome de usuário'}))
    matricula = forms.CharField(label='Matricula', max_length=4, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Matricula do professor'}))
    # TODO: Implementar os metodos _clean dos atributos do formulário