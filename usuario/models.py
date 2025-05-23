from django.db import models
from django.contrib.auth.models import User
from curso.models import Curso
import datetime
from usuario.constants import JORNADA

class Aluno(models.Model):
    usuario = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.DO_NOTHING)
    matricula = models.CharField(unique=True,max_length=6, blank=False, null=False, verbose_name='Matricula')
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING, blank=False, null=False, verbose_name='Curso')
    endereco = models.CharField(max_length=255, blank=False, null=False, verbose_name='Endereço')
    cpf = models.CharField(unique=True,max_length=11, blank=False, null=False, verbose_name='CPF')
    ingresso = models.DateField(default=datetime.date.today, null=False, blank=False, verbose_name='Data de ingresso')
    conclusao_prevista = models.DateField(default=datetime.date.today,blank=False, null=False, verbose_name='Conclusão')

    def __str__(self):
        return f'<{self.usuario}>'
    
    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'


class Professor(models.Model):
    usuario = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.DO_NOTHING)
    matricula = models.CharField(unique=True,max_length=4, blank=False, null=False, verbose_name='Matricula')
    curso = models.ForeignKey(Curso, on_delete=models.DO_NOTHING, blank=False, null=False, verbose_name='Curso')
    cpf = models.CharField(unique=True, max_length=11, blank=False, null=False, verbose_name='CPF')
    regime = models.CharField(max_length=3, blank=False, null=False, choices=JORNADA, verbose_name='Regime de trabalho')
    contratacao = models.DateField(default=datetime.date.today, blank=False, null=False, verbose_name='Data de Contratação')

    def __str__(self):
        return f'{self.usuario.first_name} {self.usuario.last_name}'

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'


class Funcionario(models.Model):
    usuario = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.CASCADE)
    matricula = models.CharField(unique=True, max_length=4, blank=False, null=False, verbose_name='Matricula')
    cpf = models.CharField(unique=True, max_length=11, blank=False, null=False, verbose_name='CPF')
    def __str__(self):
        return f'<{self.usuario}>'

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

