from django.db import models
from django.contrib.auth.models import User
from curso.models import Curso
import datetime


class Aluno(models.Model):
    usuario = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.DO_NOTHING)
    matricula = models.CharField(max_length=6, blank=False, null=False, verbose_name='Matricula')
    curso = models.CharField(max_length=25, blank=False, null=False, verbose_name='Curso')
    endereco = models.CharField(max_length=255, blank=False, null=False, verbose_name='Endereço')
    cpf = models.CharField(max_length=11, blank=False, null=False, verbose_name='CPF')
    ingresso = models.DateField(default=datetime.date.today, null=False, blank=False, verbose_name='Data de ingresso')
    conclusao_prevista = models.DateField()


class Professor(models.Model):
    JORNADA = (
        ('20', '20hr'),
        ('40', '40hr'),
        ('DE', 'DE'),
    )
    usuario = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.DO_NOTHING)
    matricula = models.CharField(max_length=4, blank=False, null=False, verbose_name='Matricula')
    curso = models.CharField(max_length=25, blank=False, null=False, verbose_name='Curso')
    cpf = models.CharField(max_length=11, blank=False, null=False, verbose_name='CPF')
    regime = models.CharField(max_length=3, blank=False, null=False, choices=JORNADA, verbose_name='Regime de trabalho')
    contratacao = models.DateField(default=datetime.date.today, blank=False, null=False, verbose_name='Data de Contratação')

class Funcionario(models.Model):
    usuario = models.ForeignKey(User, verbose_name='Usuário', on_delete=models.DO_NOTHING)
    matricula = models.CharField(max_length=4, blank=False, null=False, verbose_name='Matricula')
