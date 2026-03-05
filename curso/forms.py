from django import forms
from django.forms import ModelForm
from livro.models import *
from django.core.exceptions import ValidationError
from curso.constants import TURNOS
import re



class FormularioCurso(forms.Form):
    cod_curso = forms.CharField(label='Código do Curso', max_length=4, widget=forms.TextInput(attrs={}))
    curso = forms.CharField(label='Curso', max_length=25, widget=forms.TextInput(attrs={}))
    descricao = forms.CharField(label='Descrição', max_length=200, widget=forms.Textarea(attrs={}))
    turno = forms.ChoiceField(label='Turno', choices=TURNOS, widget=forms.Select(attrs={}))
    duracao = forms.IntegerField(label='Duração do Curso')

    # TODO: Fazer as validações de formulário