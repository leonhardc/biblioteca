from django import template
from utils.templates.utils import formatar_turno, formatar_nacionalidade, extrair_ano, formatar_cpf, extrair_mes_ano, formatar_jornada

register = template.Library()

@register.filter
def filter_formatar_turno(turno):
    return formatar_turno(turno)

@register.filter
def filter_formatar_nacionalidade(nacionalidade):
    return formatar_nacionalidade(nacionalidade)

@register.filter
def filter_extrair_ano(data_str):
    return extrair_ano(data_str)

@register.filter
def filter_extrair_mes_ano(data_str):
    return extrair_mes_ano(data_str)

@register.filter
def filter_formatar_cpf(cpf_str):
    return formatar_cpf(cpf_str)

@register.filter
def filter_formatar_jornada(jornada):
    return formatar_jornada(jornada)