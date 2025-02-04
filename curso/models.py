from django.db import models

class Curso(models.Model):
    TURNOS = (
        ('M', 'Matutino'),
        ('V', 'Vespertino'),
        ('I', 'Integral'),
    )
    cod_curso = models.CharField(max_length=4, blank=False, null=False, verbose_name='Código do Curso')
    curso = models.CharField(max_length=25, blank=False, null=False, verbose_name='Curso')
    descricao = models.TextField(max_length=200, blank=True, null=False, verbose_name='Descrição do Curso')
    turno = models.CharField(max_length=1, choices=TURNOS, blank=False, null=False, verbose_name='Turno', default='M')
    class Meta:
        verbose_name = 'Curso'  
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.curso

    

