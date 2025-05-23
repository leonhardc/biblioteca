from curso.models import Curso

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