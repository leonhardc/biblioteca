from datetime import datetime, timedelta
from usuario.forms import FormularioAluno
from usuario.models import Aluno, Professor, Funcionario
import random
import re

def gerar_data():
    data_inicio = datetime(1900, 1, 1)  
    data_fim = datetime(2025, 12, 31)   
    dias_aleatorios = random.randint(0, (data_fim - data_inicio).days)
    return data_inicio + timedelta(days=dias_aleatorios)

def separar_endereco(endereco:str):
    """
        Formato de endereço aceito:
        f'{tipo_logadouro} {logadouro}, {numero}, {complemento} - {bairro}. CEP: {cep}. {cidade}/{estado}'
    """
    try:
        logradouro, numero, outros = endereco.split(',')
        complemento_bairro, cep, cidade_estado = outros.split('.')
        complemento, bairro = complemento_bairro.split('-')
        cidade, estado = cidade_estado.split('/')

        tipo_logradouro = logradouro.split(' ')[0].strip()
        logradouro = ' '.join(logradouro.split(' ')[1:]).strip()
        numero = numero.strip()
        complemento = complemento.strip()
        bairro = bairro.strip()
        cep = ''.join([dig for dig in cep if dig.isdigit()])
        cidade = cidade.strip()
        estado = estado.strip()
        return {
            'tipo_logradouro':tipo_logradouro,
            'logradouro':logradouro, 
            'numero':numero, 
            'complemento':complemento, 
            'bairro':bairro,
            'cep':cep, 
            'cidade':cidade, 
            'estado':estado, 
            }
    except:
        return {
            'tipo_logradouro': '',
            'logradouro':'', 
            'numero':'', 
            'complemento':'', 
            'bairro':'',
            'cep':'', 
            'cidade':'', 
            'estado':'', 
        } 
    
def informacoes_formulario_aluno(aluno:Aluno, endereco):
    data = {
        'nome' : aluno.usuario.first_name,
        'sobrenome' : aluno.usuario.last_name,
        'email' : aluno.usuario.email,
        'usuario' : aluno.usuario.username,
        'tipo_logradouro' : endereco['tipo_logradouro'],
        'logradouro' : endereco['logradouro'],
        'numero' : endereco['numero'],
        'bairro' : endereco['bairro'],
        'cidade' : endereco['cidade'],
        'estado' : endereco['estado'],
        'cep' : endereco['cep'],
        'complemento' : endereco['complemento'],
        'matricula' : aluno.matricula,
        'curso' : aluno.curso.cod_curso,
        'ingresso' : aluno.ingresso,
        'conclusao_prevista' : aluno.conclusao_prevista
    }
    return data

def informacoes_formulario_professor(professor:Professor):
    data = {
        'nome': professor.usuario.first_name,
        'sobrenome': professor.usuario.last_name,
        'email': professor.usuario.email,
        'usuario': professor.usuario.username,
        'matricula': professor.matricula,
        'curso': professor.curso.cod_curso,
        'cpf': professor.cpf,
        'regime': professor.regime,
        'contratacao': professor.contratacao
    }
    return data

def informacoes_formulario_funcionario(funcionario:Funcionario):
    data = {
        'nome': funcionario.usuario.first_name,
        'sobrenome': funcionario.usuario.last_name,
        'email': funcionario.usuario.email,
        'usuario': funcionario.usuario.username,
        'matricula': funcionario.matricula,
        'cpf': funcionario.cpf
    }
    return data

def formatar_endereco(formulario):
    tipo_logadouro = formulario.cleaned_data['tipo_logradouro']
    logadouro = formulario.cleaned_data['logradouro']
    numero = formulario.cleaned_data['numero']
    bairro = formulario.cleaned_data['bairro']
    cep = formulario.cleaned_data['cep']
    cidade = formulario.cleaned_data['cidade']
    estado = formulario.cleaned_data['estado']
    complemento = formulario.cleaned_data['complemento']
    return f'{tipo_logadouro} {logadouro}, {numero}, {complemento} - {bairro}. CEP: {cep}. {cidade}/{estado}'

def gerar_matricula_aluno():
    while(True):
        matricula = f'{random.randint(100000, 999999)}'
        aluno = Aluno.objects.get(matricula=matricula)
        if not aluno:
            break
    return matricula

def gerar_matricula_professor():
    while(True):
        matricula = f'{random.randint(1000, 9999)}'
        professor = Aluno.objects.get(matricula=matricula)
        if not professor:
            break
    return matricula
