from django import forms
from django.forms import ModelForm
from livro.models import *
from django.core.exceptions import ValidationError
import re

CATEGORIAS = tuple([(categoria.id, categoria.categoria) for categoria in Categoria.objects.all()])
AUTORES =  tuple([(autor.id, autor.nome) for autor in Autor.objects.all()])

class FormularioLivro(forms.Form):
    isbn = forms.CharField(label='ISBN', max_length=6, widget=forms.TextInput(attrs={'placeholder':'Digite o numero de ISBN'}))
    titulo = forms.CharField(label='Titulo', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Digite o titulo do livro'}))
    subtitulo = forms.CharField(label='Subtitulo', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Digite o subtitulo do livro'}))
    lancamento = forms.DateField(label='Ano de Lançamento', widget=forms.DateInput())
    editora = forms.CharField(label='Editora', widget=forms.TextInput(attrs={'placeholder':'Digite a Editora do livro'}))    
    copias = forms.IntegerField(label='Quantidade de cópias', max_value=999, min_value=0)
    autores = forms.ChoiceField(label='Autores', choices=AUTORES, widget=forms.SelectMultiple())
    categoria = forms.ChoiceField(label='Categoria', choices=CATEGORIAS, widget=forms.Select(attrs={}))

class FormularioAutor(forms.ModelForm):
    pass

class FormularioCategoria(forms.ModelForm):
    pass

class FormularioReserva(forms.ModelForm):
    pass

class FormularioEmprestimo(forms.ModelForm):
    pass