from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

NACIONALIDADES = (
    ('1', 'Portuguesa'),
    ('2', 'Filipina'),
    ('3', 'Sul-Africano'),
    ('4', 'Zimbabweano'),
    ('5', 'Namibiana'),
    ('6', 'Boliviano'),
    ('7', 'Brasileiro'),
    ('8', 'Chileno'),
    ('9', 'Colombiano'),
    ('10', 'Costarriquenho'),
    ('11', 'Cubano'),
    ('12', 'Dominicano'),
    ('13', 'Equatoriano'),
    ('14', 'Salvadorenho'),
    ('15', 'Granadino'),
    ('16', 'Guatemalteco'),
    ('17', 'Guianês'),
    ('18', 'Guianense'),
    ('19', 'Haitiano'),
    ('20', 'Hondurenho'),
    ('21', 'Jamaicano'),
    ('22', 'Mexicano'),
    ('23', 'Nicaraguense'),
    ('24', 'Panamenho'),
    ('25', 'Paraguaio'),
    ('26', 'Peruano'),
    ('27', 'Portorriquenho'),
    ('28', 'Dominicana'),
    ('29', 'São-cristovense'),
    ('30', 'São-vicentino'),
    ('31', 'Santa-lucense'),
    ('32', 'Surinamês'),
    ('33', 'Trindadense'),
    ('34', 'Uruguaio'),
    ('35', 'Venezuelano'),
    ('36', 'Alemã'),
    ('37', 'Austríac'),
    ('38', 'Belga'),
    ('39', 'Croata'),
    ('40', 'Dinamarquês'),
    ('41', 'Antiguano'),
    ('42', ' Argentino'),
    ('43', 'Bahamense'),
    ('44', 'barbadense'),
    ('45', 'Belizenho'),
    ('46', 'Eslovaco'),
    ('47', 'Esloveno'),
    ('48', 'Espanhol'),
    ('49', 'Francês'),
    ('50', 'Grego'),
    ('51', 'Húngaro'),
    ('52', 'Irlandês'),
    ('53', 'Italiano'),
    ('54', 'Noruego'),
    ('55', 'Holandês'),
    ('56', 'Polonês'),
    ('57', 'Inglês'),
    ('58', 'Galês'),
    ('59', 'Escocês'),
    ('60', 'Romeno'),
    ('61', 'Russo'),
    ('62', 'Sérvio'),
    ('63', 'Sueco'),
    ('64', 'Suíço'),
    ('65', 'Turco'),
    ('66', 'Ucraniano'),
    ('67', 'Americano'),
    ('68', 'Canadense'),
    ('69', 'Angolano'),
    ('70', 'Moçambicano'),
    ('71', 'Sul-africano'),
    ('72', 'Zimbabuense'),
    ('73', 'Argélia'),
    ('74', 'Comorense'),
    ('75', 'Egípcio'),
    ('76', 'Líbio'),
    ('77', 'Marroquino'),
    ('78', 'Ganés'),
    ('79', 'Queniano'),
    ('80', 'Ruandês'),
    ('81', 'Ugandense'),
    ('82', 'Bechuano'),
    ('83', 'Marfinense'),
    ('84', 'Camaronense'),
    ('85', 'Nigeriano'),
    ('86', 'Somali'),
    ('87', 'Australiano'),
    ('88', 'Neozelandês'),
    ('89', 'Afegão'),
    ('90', 'Saudita'),
    ('91', 'Armeno'),
    ('92', 'Bangladesh'),
    ('93', 'Chinês'),
    ('94', 'Norte-coreano'),
    ('95', 'Sul-coreano'),
    ('96', 'Indiano'),
    ('97', 'Indonésio'),
    ('98', 'Iraquiano'),
    ('99', 'Iraniano'),
    ('100', 'Israelita'),
    ('101', 'Japonês'),
    ('102', 'Malaio'),
    ('103', 'Nepalês'),
    ('104', 'Omanense'),
    ('105', 'Paquistanês'),
    ('106', 'Palestino'),
    ('107', 'Qatarense'),
    ('108', 'Sírio'),
    ('109', 'Cingalês'),
    ('110', 'Tailandês'),
    ('111', 'Timorense'),
    ('112', 'Árabe'),
    ('113', 'Vietnamita'),
    ('114', 'Iemenita')
)


class Autor(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nome do Autor')
    cpf = models.CharField(default='00000000000',max_length=11, blank=True, null=False, verbose_name='CPF do Autor')
    nacionalidade = models.CharField(max_length=3, choices=NACIONALIDADES, verbose_name='Nacionalidade')
    
    def __str__(self):
        return f'{self.nome}'
    
    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'


class Categoria(models.Model):
    categoria = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nome da Categoria')
    descricao = models.TextField()
    
    def __str__(self):
        return f'{self.categoria}'



class Livro(models.Model):
    isbn = models.CharField(max_length=6, blank=False, null=False, verbose_name='ISBN')
    titulo = models.CharField(max_length=100, blank=False, null=False, verbose_name='Titulo')
    subtitulo = models.CharField(max_length=250, blank=False, null=False, verbose_name='Subtitulo')
    lancamento = models.DateField(verbose_name='Ano de Lançamento')
    editora = models.CharField(max_length=100, blank=False, null=False, verbose_name='Editora')
    copias = models.IntegerField(blank=False, null=False, verbose_name='Quantidade de Cópias')
    autores = models.ManyToManyField(Autor, verbose_name='Autores')
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name='Categoria')
    
    def get_autores(self):
        return ', '.join([autor.nome for autor in self.autores.all()])

    def __str__(self):
        return f'{self.id}:{self.titulo}'


class Reserva(models.Model):
    usuario = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, verbose_name='Usuário')
    livro = models.ForeignKey(Livro, blank=False, null=False,on_delete=models.CASCADE, verbose_name='Livro')
    data_reserva = models.DateField(default=timezone.now, blank=False, null=False, verbose_name='Data da Reserva')


class Emprestimo(models.Model):
    usuario = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, verbose_name='Usuário')
    livro = models.ForeignKey(Livro, blank=False, null=False,on_delete=models.CASCADE, verbose_name='Livro')
    data_emprestimo = models.DateField(default=timezone.now, blank=False, null=False, verbose_name='Data da Reserva')
    # TODO: Implementar a regra de devolução
    # * Um ALUNO pode pedir emprestado até 3 livros emprestados por até 15 dias cada.
    # * Um PROFESSOR pode pedir até 5 livros emprestados por até 30 dias cada.
    # * Um FUNCIONARIO pode pedir até 4 livros emprestados por até 21 dias cada.
    data_devolucao = models.DateField(default=timezone.now, blank=False, null=False, verbose_name='Data da Devolução')
