from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from livro.constants import NACIONALIDADES



SEXO = (
    ('M', 'Masculino'),
    ('F', 'Feminino')
)

class Autor(models.Model):
    nome = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nome do Autor')                      # type: ignore
    sobrenome = models.CharField(max_length=100, blank=False, null=False, verbose_name="Sobrenone do Autor") # type: ignore
    email_de_contato = models.EmailField(blank=False, null=False, verbose_name='Email de contato do Autor')
    nascimento = models.DateTimeField(verbose_name='Data de Nascimento do Autor')
    sexo = models.CharField(max_length=1, choices=SEXO, verbose_name="Sexo do Autor")
    nacionalidade = models.CharField(max_length=3, choices=NACIONALIDADES, verbose_name='Nacionalidade')                # type: ignore
    
    def __str__(self):
        return f'{self.nome}'                                                                                            # type: ignore
    
    class Meta:
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'


class Categoria(models.Model):
    categoria = models.CharField(max_length=100, blank=False, null=False, verbose_name='Nome da Categoria') # type: ignore
    descricao = models.TextField()                                                                          # type: ignore
    
    def __str__(self):
        return f'{self.categoria}'                                                                          # type: ignore


class Livro(models.Model):
    isbn = models.CharField(max_length=6, blank=False, null=False, verbose_name='ISBN')                         # type: ignore
    titulo = models.CharField(max_length=100, blank=False, null=False, verbose_name='Titulo')                   # type: ignore
    subtitulo = models.CharField(max_length=250, blank=False, null=False, verbose_name='Subtitulo')             # type: ignore
    lancamento = models.DateField(verbose_name='Ano de Lançamento')                                             # type: ignore
    editora = models.CharField(max_length=100, blank=False, null=False, verbose_name='Editora')                 # type: ignore
    copias = models.IntegerField(blank=False, null=False, verbose_name='Quantidade de Cópias')                  # type: ignore
    autores = models.ManyToManyField(Autor, verbose_name='Autores')                                             # type: ignore
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING, verbose_name='Categoria')             # type: ignore
    
    def get_autores(self):
        return ', '.join([autor.nome for autor in self.autores.all()])  # type: ignore

    def __str__(self):
        return f'{self.titulo}'                               # type: ignore


class Reserva(models.Model):
    usuario = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, verbose_name='Usuário')    # type: ignore
    livro = models.ForeignKey(Livro, blank=False, null=False,on_delete=models.CASCADE, verbose_name='Livro')        # type: ignore
    data_reserva = models.DateField(default=timezone.now, blank=False, null=False, verbose_name='Data da Reserva')  # type: ignore
    ativo = models.BooleanField(default=True, verbose_name="Reserva Ativa") # type: ignore


class Emprestimo(models.Model):
    usuario = models.ForeignKey(User, blank=False, null=False, on_delete=models.CASCADE, verbose_name='Usuário')        # type: ignore
    livro = models.ForeignKey(Livro, blank=False, null=False,on_delete=models.CASCADE, verbose_name='Livro')            # type: ignore
    data_emprestimo = models.DateField(default=timezone.now, blank=False, null=False, verbose_name='Data da Reserva')   # type: ignore
    ativo = models.BooleanField(default=True, verbose_name="Emprestimo Ativo") # type: ignore
    # TODO: Implementar a regra de devolução
    # * Um ALUNO pode pedir emprestado até 3 livros emprestados por até 15 dias cada.
    # * Um PROFESSOR pode pedir até 5 livros emprestados por até 30 dias cada.
    # * Um FUNCIONARIO pode pedir até 4 livros emprestados por até 21 dias cada.
    data_devolucao = models.DateField(default=timezone.now, blank=False, null=False, verbose_name='Data da Devolução')  # type: ignore
