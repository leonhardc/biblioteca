from django import forms
from usuario.models import Aluno

class LoginForm(forms.Form):
    usuario = forms.CharField(label='Usuário', max_length=255, 
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usuário', 'style': 'background-color:#e5ebf4'}))
    senha = forms.CharField(label='Senha', max_length=255, 
                            widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Senha', 'style': 'background-color:#e5ebf4'}))
    
class FormularioAluno(forms.Form):
    # Dados Pessoais
    nome = forms.CharField(label='Nome', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Insira o nome do aluno'}))
    sobrenome = forms.CharField(label='Sobrenome', max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Insira o sobrenome do aluno'}))
    email = forms.CharField(label='Email', max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email do aluno'}))
    usuario = forms.CharField(label='Usuário', max_length=20, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Insira seu nome de usuário'}))
    senha = forms.CharField(label='Senha', max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Insira sua Senha'}))
    senha_confirmacao = forms.CharField(label='Senha', max_length=50, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirme sua senha'}))
    matricula=forms.CharField(label='Matricula', max_length=6, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Insira a matricula do Aluno'}))
    data_nascimento = forms.DateField(label='Data de Nascimento', widget=forms.DateInput(attrs={'class':'form-control'}))
    # Endereço
    rua = forms.CharField(label='Rua', max_length=100, widget=forms.TextInput(attrs={'class':'form-control'}))
    numero= forms.CharField(label='Numero',max_length=6,widget=forms.TextInput(attrs={'class':'form-control'}))
    bairro= forms.CharField(label='Bairro',max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    cidade = forms.CharField(label='Cidade',max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    estado= forms.CharField(label='Estado',max_length=50,widget=forms.TextInput(attrs={'class':'form-control'}))
    cep = forms.CharField(label='CEP',max_length=8,widget=forms.TextInput(attrs={'class':'form-control'}))
    complemento= forms.CharField(label='Complemento',max_length=200,widget=forms.TextInput(attrs={'class':'form-control'}))
    # Curso
    matricula = forms.CharField(label='Matricula', max_length=6,widget=forms.TextInput(attrs={'class':'form-control'}))
    curso = forms.CharField(label='Curso', max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))