from django import template
from utils.templates.utils_templates import formatar_turno, formatar_nacionalidade, extrair_ano, formatar_cpf, extrair_mes_ano, formatar_jornada # type: ignore

register = template.Library()

@register.filter
def filter_formatar_turno(turno:str):
    return formatar_turno(turno)

@register.filter
def filter_formatar_nacionalidade(nacionalidade:str):
    return formatar_nacionalidade(nacionalidade)

@register.filter
def filter_extrair_ano(data_str:str):
    return extrair_ano(data_str)

@register.filter
def filter_extrair_mes_ano(data_str:str):
    return extrair_mes_ano(data_str)

@register.filter
def filter_formatar_cpf(cpf_str:str):
    return formatar_cpf(cpf_str)

@register.filter
def filter_formatar_jornada(jornada:str):
    return formatar_jornada(jornada)