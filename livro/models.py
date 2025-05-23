from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from livro.constants import NACIONALIDADES



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
