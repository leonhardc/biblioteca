from django.db import models
from curso.constants import TURNOS

class Curso(models.Model):
    cod_curso = models.CharField(unique=True,max_length=8, blank=False, null=False, verbose_name='Código do Curso')
    curso = models.CharField(max_length=25, blank=False, null=False, verbose_name='Curso')
    descricao = models.TextField(max_length=200, blank=True, null=False, verbose_name='Descrição do Curso')
    turno = models.CharField(max_length=1, choices=TURNOS, blank=False, null=False, verbose_name='Turno', default='M')
    duracao = models.IntegerField(default=5,blank=False, null=False, verbose_name='Duração')

    class Meta:
        verbose_name = 'Curso'  
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.curso

    

