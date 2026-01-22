from django import forms
from livro.models import Categoria
from livro.constants import NACIONALIDADES
from livro.models import Categoria
from livro.models import Autor
from livro.models import Livro

def get_categorias() -> tuple[tuple[int, str]]:
    try:
        return tuple([(categoria.id, categoria.categoria) for categoria in Categoria.objects.all()])  # type: ignore
    except: 
        return () # type: ignore

def get_autores() -> tuple[tuple[int, str]]:
    try:
        return tuple([(autor.id, autor.nome) for autor in Autor.objects.all()])                         # type: ignore
    except:
        return () # type: ignore

def get_livros() -> tuple[tuple[int, str]]:
    try:
        return tuple([(livro.id, livro.titulo) for livro in Livro.objects.all()])  # type: ignore
    except:
        return () # type: ignore

def get_usuarios() -> tuple[tuple[int, str]]:
    from django.contrib.auth.models import User
    try:
        return tuple([(usuario.id, usuario.username) for usuario in User.objects.all()])                 # type: ignore
    except:
        return ()  # type: ignore

# # Constantes de Formulários.

CATEGORIAS = get_categorias()
AUTORES =  get_autores() 
USUARIOS = get_usuarios() 
LIVROS = get_livros()

class FormularioLivro(forms.Form):
    isbn = forms.CharField(
        label='ISBN', 
        max_length=6, 
        widget=forms.TextInput(attrs={'placeholder':'Digite o numero de ISBN'})
    )
    titulo = forms.CharField(
        label='Titulo', 
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder':'Digite o titulo do livro'})
    )
    subtitulo = forms.CharField(
        label='Subtitulo', 
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder':'Digite o subtitulo do livro'})
    )
    lancamento = forms.DateField(label='Ano de Lançamento', widget=forms.DateInput())
    editora = forms.CharField(
        label='Editora', 
        widget=forms.TextInput(attrs={'placeholder':'Digite a Editora do livro'})
    )    
    copias = forms.IntegerField(label='Quantidade de cópias', max_value=999, min_value=0)
    autores = forms.MultipleChoiceField(label='Autores', choices=AUTORES, widget=forms.SelectMultiple())    # type: ignore
    categoria = forms.ChoiceField(label='Categoria', choices=CATEGORIAS, widget=forms.Select(attrs={}))     # type: ignore

    def clean_categoria(self):
        categoria_id = self.cleaned_data['categoria']
        categoria = Categoria.objects.get(id=categoria_id)
        if not categoria:
            raise forms.ValidationError('Categoria não existe na base de dados.')
        return categoria

class FormularioAutor(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100, widget=forms.TextInput())
    cpf = forms.CharField(label='CPF', max_length=100, widget=forms.TextInput())
    nacionalidade = forms.ChoiceField(label='Nome', choices=NACIONALIDADES, widget=forms.Select())

class FormularioCategoria(forms.Form):
    categoria = forms.CharField(label='Categoria', max_length=100, widget=forms.TextInput())
    descricao = forms.CharField(label='Descrição', max_length=2000, widget=forms.Textarea())

class FormularioReserva(forms.Form):
    usuario = forms.ChoiceField(label='Usuário', choices=USUARIOS,widget=forms.Select())                                # type: ignore
    livro = forms.ChoiceField(label='Livro', choices=LIVROS, widget=forms.Select())                                     # type: ignore
    data_reserva = forms.DateField(label='Data da Reserva', widget=forms.DateInput(attrs={'type':'date'}))              # type: ignore

class FormularioCriarEmprestimo(forms.Form):
    usuario = forms.ChoiceField(label='Usuário', choices=get_usuarios(),widget=forms.Select())                                # type: ignore
    livro = forms.ChoiceField(label='Livro', choices=get_livros(), widget=forms.Select())                                     # type: ignore
    data_emprestimo = forms.DateField(label='Data da Reserva', widget=forms.DateInput(attrs={'type':'date'}))           # type: ignore
    # data_devolucao = forms.DateField(label='Data da Reserva', widget=forms.DateInput(attrs={'type':'date'}))            # type: ignore

class FormularioAtualizarEmprestimo(forms.Form):
    usuario = forms.ChoiceField(label='Usuário', choices=get_usuarios(),widget=forms.Select(attrs={'disabled':True}))                                # type: ignore
    livro = forms.ChoiceField(label='Livro', choices=get_livros(), widget=forms.Select())                                     # type: ignore
    data_emprestimo = forms.DateField(label='Data da Reserva', widget=forms.DateInput(attrs={'type':'date'}))           # type: ignore
    data_devolucao = forms.DateField(label='Data da Devolução', widget=forms.DateInput(attrs={'type':'date'}))            # type: ignore

class FormularioRenovarEmprestimo(forms.Form):
    usuario = forms.ChoiceField(label='Usuário', choices=get_usuarios(),widget=forms.Select(attrs={'disabled':False})) # type: ignore

class FormularioRegistrarDevolucao(forms.Form):
    usuario = forms.ChoiceField(label='Usuário', choices=get_usuarios(),widget=forms.Select(attrs={'disabled':False})) # type: ignore