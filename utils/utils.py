from datetime import datetime, timedelta
import random

def gerar_data():
    data_inicio = datetime(1900, 1, 1)  # Data mínima (1º de janeiro de 1900)
    data_fim = datetime(2025, 12, 31)   # Data máxima (31 de dezembro de 2025)

    # Gerar um número aleatório de dias dentro do intervalo
    dias_aleatorios = random.randint(0, (data_fim - data_inicio).days)

    # Retornar a data aleatória
    return data_inicio + timedelta(days=dias_aleatorios)