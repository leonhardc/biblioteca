# from curso.models import Curso

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

lista_de_cursos = [
        ('ENGCOMP','Engenharia de Computação'),
        ('ENGELE','Engenharia Eletrica'),
        ('MUSIC','Musica'),
        ('ECON','Economia'),
        ('ODONTO','Odontologia'),
        ('MED','Medicina'),
        ('ENFER','Enfermagem'),        
    ]

OPCOES_CURSOS = tuple(lista_de_cursos)

JORNADA = (
        ('20', '20hr'),
        ('40', '40hr'),
        ('DE', 'Dedicação Exclusiva'),
    )

LOGRADOUROS = (
    ('R.', 'Rua'),
    ('Av.', 'Avenida'),
    ('Al.', 'Alameda'),
    ('Pca.', 'Praça'),
    ('Rod.', 'Rodovia'),
    ('AVC','Avenida Contorno'),
    ('AVM', 'Avenida Marginal'),
    ('AVV', 'Avenida Velha'),
    ('Aeroporto', 'Aeroporto'),
    ('Área', 'Área'), 
    ('Campo', 'Campo'),
    ('Chácara', 'Chácara'),
    ('Colônia', 'Colônia'),
    ('Condomínio', 'Condomínio'),
    ('Conjunto', 'Conjunto'),
    ('Distrito', 'Distrito'),
    ('Esplanada', 'Esplanada'),
    ('Estação', 'Estação')
)

MAX_EMPRESTIMOS_POR_USUARIO = {
    'aluno': 4,
    'professore': 5,
    'funcionario': 4,    
}
NUM_MAX_EMPRESTIMOS = {
    'aluno': 4,
    'professore': 5,
    'funcionario': 4,    
}

NUM_MAX_DIAS_EMPRESTIMOS = {
    'aluno': 15,
    'professore': 30,
    'funcionario': 21
}

MAX_RESERVAS_POR_USUARIO = {
    'aluno': 10,
    'professor': 15,
    'funcionario': 12,
}

USUARIO_NAO_AUTENTICADO = 'O usuario nao esta autenticado.'
OPERACAO_INVALIDA = 'Operação Inválida.'