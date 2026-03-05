from curso.constants import TURNOS
from livro.constants import NACIONALIDADES
from usuario.constants import JORNADA
from datetime import datetime, date

MESES = (
    (1, 'Janeiro'),
    (2, 'Fevereiro'),
    (3, 'Março'),
    (4, 'Abril'),
    (5, 'Maio'),
    (6, 'Junho'),
    (7, 'Julho'),
    (8, 'Agosto'),
    (9, 'Setembro'),
    (10, 'Outubro'),
    (11, 'Novembro'),
    (12, 'Dezembro'),
)


def formatar_turno(turno:str):
    if turno:
        return dict(TURNOS)[turno]
    return turno


def formatar_nacionalidade(nacionalidade:str):
    if nacionalidade:
        return dict(NACIONALIDADES)[nacionalidade]
    return nacionalidade


def extrair_ano(data_str:str):
    try:
        if isinstance(data_str, (datetime, date)):
            return data_str.year
        data = datetime.strptime(data_str, "%d de %B de %Y")
        return data.year
    except ValueError:
        return data_str


def extrair_mes_ano(data_str:str):
    try:
        if isinstance(data_str, (datetime, date)):
            return f'{dict(MESES)[data_str.month]} de {data_str.year}'
        
        data = datetime.strptime(data_str, "%d de %B de %Y")
        return f'{data.month} de {data.year}'
    except ValueError:
        return data_str


def formatar_cpf(cpf_str:str):
    return f'{cpf_str[0:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:]}'


def formatar_jornada(jornada:str):
    if jornada:
        return dict(JORNADA)[jornada]
    return jornada