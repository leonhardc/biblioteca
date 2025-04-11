from datetime import datetime, timedelta
from usuario.forms import FormularioAluno
from usuario.models import Aluno, Professor
import random

def gerar_data():
    data_inicio = datetime(1900, 1, 1)  
    data_fim = datetime(2025, 12, 31)   
    dias_aleatorios = random.randint(0, (data_fim - data_inicio).days)
    return data_inicio + timedelta(days=dias_aleatorios)

def separar_endereco(endereco:str):
    try:
        rua, numero, cidade, outros = endereco.split(",")
        rua = rua.strip()
        numero = numero.strip()
        cidade = cidade.strip()
        outros = outros.strip()
        outros, estado = outros.split('/')
        estado = estado.strip()
        cep =  outros.split(' ')[0].strip()
        bairro =  " ".join(outros.split(" ")[1:]).strip()
        return {'rua':rua, 'numero':numero, 'cidade':cidade, 'estado':estado, 'cep':cep, 'bairro':bairro}
    except:
        return {'rua':'', 'numero':'', 'cidade':'', 'estado':'', 'cep':'', 'bairro':''}

def informacoes_formulario_aluno(aluno:Aluno, endereco):
    data = {
        'nome' : aluno.usuario.first_name,
        'sobrenome' : aluno.usuario.last_name,
        'email' : aluno.usuario.email,
        'usuario' : aluno.usuario.username,
        'rua' : endereco['rua'],
        'numero' : endereco['numero'],
        'bairro' : endereco['bairro'],
        'cidade' : endereco['cidade'],
        'estado' : endereco['estado'],
        'cep' : endereco['cep'],
        'complemento' : aluno.complemento,
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
        'username': professor.usuario.username,
        'matricula': professor.matricula,
        'curso': professor.curso.cod_curso,
        'cpf': professor.cpf,
        'regime': professor.regime,
        'contratacao': professor.contratacao
    }
    return data