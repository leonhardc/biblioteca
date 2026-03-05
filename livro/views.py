from pprint import pprint
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
# from django.contrib.auth.decorators import entrar_required
from .models import Livro
from datetime import date
from utils.utils import *
from django.db.models import Q
from usuario.constants import MAX_RESERVAS_POR_USUARIO, MAX_EMPRESTIMOS_POR_USUARIO, NUM_MAX_DIAS_EMPRESTIMOS
from livro.constants import NUMERO_MAXIMO_DE_RENOVACOES_POR_USUARIO
from utils.usuarios.utils import user_is_aluno, user_is_professor, user_is_funcionario
from utils.livros.utils import criar_reserva_aluno, criar_reserva_professor, criar_reserva_funcionario
from .forms import *
# Método de Listar Livros, Autores e Categorias
def listar_livros(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        user_context = {
            'aluno': user_is_aluno(request.user),
            'professor': user_is_professor(request.user),
            'funcionario': user_is_funcionario(request.user),
        }
        template_name = "livro/livros.html"
        itens_por_pagina = 21
        termo_pesquisa = request.GET.get("pesquisa", "").strip()
        pesquisa_categoria = request.GET.get("categoria", "").strip()
        livros_queryset = Livro.objects.select_related(
            'categoria'
        ).prefetch_related(
            'autores'
        )
        
        # Aplicar filtros de pesquisa se necessário
        if termo_pesquisa:
            livros_queryset = livros_queryset.filter(
                Q(titulo__icontains=termo_pesquisa) |
                Q(subtitulo__icontains=termo_pesquisa) |
                Q(autores__nome__icontains=termo_pesquisa)
            ).distinct()  # distinct() necessário por causa do ManyToMany com autores
        
        if pesquisa_categoria:
            livros_queryset = livros_queryset.filter(categoria__id=pesquisa_categoria)
        
        # Ordenação consistente (importante para paginação)
        livros_queryset = livros_queryset.order_by('-id')
        
        # Paginação otimizada
        paginator = Paginator(livros_queryset, itens_por_pagina)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        
        context = {
            "livros": page_obj,
            "termo_busca": termo_pesquisa,
            "pesquisa_categoria": pesquisa_categoria,
            "total_resultados": paginator.count,
            'user_context': user_context,
        }
        
        return render(request, template_name, context)
    else:
        messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não está autenticado.')
        return redirect('usuario:entrar')

def listar_autores(request:HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            termo_pesquisa = request.GET.get("pesquisa", "").strip()
            if termo_pesquisa:
                autores_queryset = Autor.objects.filter(
                    Q(nome__icontains=termo_pesquisa) |
                    Q(sobrenome__icontains=termo_pesquisa)
                ).distinct().order_by('nome')
                user_context = {
                    'aluno': user_is_aluno(request.user),
                    'professor': user_is_professor(request.user),
                    'funcionario': user_is_funcionario(request.user),
                }
                template_name = "livro/listar_autores.html"
                if autores_queryset.exists():
                    return render(request, template_name=template_name, context={'autores':autores_queryset, 'user_context': user_context})
                else:
                    messages.add_message(request, messages.ERROR, 'Nenhum autor encontrado para o termo de pesquisa informado.')
                    return render(request, template_name, context={'autor':True, 'user_context': user_context})
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            template_name = "livro/listar_autores.html"
            autores_existem = Autor.objects.all().exists()
            if autores_existem:
                autores = Autor.objects.all().order_by('nome')
                return render(request, template_name=template_name, context={'autores':autores, 'user_context': user_context})
            else:
                messages.add_message(request, messages.ERROR, 'Não existem autores cadastrados na biblioteca.')
                return render(request, template_name, context={'autor':True, 'user_context': user_context})
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def listar_categorias(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            termo_pesquisa = request.GET.get("pesquisa", "").strip()
            if termo_pesquisa:
                categorias_queryset = Categoria.objects.filter(
                    Q(categoria__icontains=termo_pesquisa) |
                    Q(descricao__icontains=termo_pesquisa)
                ).distinct().order_by('categoria')
                user_context = {
                    'aluno': user_is_aluno(request.user),
                    'professor': user_is_professor(request.user),
                    'funcionario': user_is_funcionario(request.user),
                }
                template_name = "livro/listar_categorias.html"
                if categorias_queryset.exists():
                    return render(request, template_name=template_name, context={'categorias':categorias_queryset, 'user_context': user_context})
                else:
                    messages.add_message(request, messages.ERROR, 'Nenhuma categoria encontrada para o termo de pesquisa informado.')
                    return render(request, template_name, context={'categoria':True, 'user_context': user_context})
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            template_name = "livro/listar_categorias.html"
            categorias_existem = Categoria.objects.all().exists()
            if categorias_existem:
                categorias = Categoria.objects.all().order_by('categoria')
                return render(request, template_name=template_name, context={'categorias':categorias, 'user_context': user_context})
            else:
                messages.add_message(request, messages.ERROR, 'Não existem categorias cadastradas na biblioteca.')
                return render(request, template_name, context={'categoria':True, 'user_context': user_context})
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')


# FUNCAO AUXILIAR
def criar_isbn() -> str:
    import random
    isbn = ''
    while True:
        isbn = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        livro_existe = Livro.objects.filter(isbn=isbn).exists()
        if not livro_existe:
            break
    return isbn

# Implementação do CRUD para livro
def criar_livro(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            if request.method == 'GET':
                user_context = {
                    'aluno': user_is_aluno(request.user),
                    'professor': user_is_professor(request.user),
                    'funcionario': user_is_funcionario(request.user),
                }
                template_name = "livro/criar_livro.html"
                formulario_livro = FormularioLivro()
                return render(request, template_name, context={'form': formulario_livro, 'user_context': user_context})
            if request.method == 'POST':
                formulario_livro = FormularioLivro(request.POST)
                if formulario_livro.is_valid():
                    isbn = criar_isbn()
                    titulo = formulario_livro.cleaned_data['titulo']
                    resumo = formulario_livro.cleaned_data['resumo']
                    subtitulo = formulario_livro.cleaned_data['subtitulo']
                    lancamento = formulario_livro.cleaned_data['lancamento']
                    editora = formulario_livro.cleaned_data['editora']
                    copias = formulario_livro.cleaned_data['copias']
                    autores = formulario_livro.cleaned_data['autores']
                    categoria = Categoria.objects.get(id=formulario_livro.cleaned_data['categoria'])
                    novo_livro = Livro.objects.create(
                        isbn=isbn,
                        titulo=titulo,
                        resumo=resumo,
                        subtitulo=subtitulo,
                        lancamento=lancamento,
                        editora=editora,
                        copias=copias,
                        categoria=categoria
                    )
                    novo_livro.autores.set(autores)
                    novo_livro.save()
                    messages.add_message(request, messages.SUCCESS, 'Livro criado com sucesso.')
                    return redirect('livro:listar_livros')
                else:
                    print(formulario_livro.errors)
                    user_context = {
                        'aluno': user_is_aluno(request.user),
                        'professor': user_is_professor(request.user),
                        'funcionario': user_is_funcionario(request.user),
                    }
                    messages.add_message(request, messages.ERROR, 'Erro ao criar o livro. Verifique os dados informados.')
                    template_name = "livro/criar_livro.html"
                    return render(request, template_name, context={'form': formulario_livro, 'user_context': user_context})
        else:
            messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não está autenticado.')
        return redirect('usuario:entrar')

def detalhar_livro(request: HttpRequest, id_livro:int) -> HttpResponse:
    if request.user.is_authenticated:
        user_context = {
            'aluno': user_is_aluno(request.user),
            'professor': user_is_professor(request.user),
            'funcionario': user_is_funcionario(request.user),
        }
        livro = Livro.objects.filter(id=id_livro).exists()
        if livro:
            livro = Livro.objects.get(id=id_livro)
            template_name = "livro/detalhar_livro.html"
            return render(request, template_name, context={'livro':livro, 'user_context': user_context})
        else:
            messages.add_message(request, messages.ERROR, 'Livro não encontrado.')
            return redirect('livro:listar_livros')
    else:
        messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não está autenticado.')
        return redirect('usuario:entrar')

def atualizar_livro(request:HttpRequest, id_livro:int) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            template_name = "livro/atualizar_livro.html"
            if request.method == 'GET':
                livro_existe = Livro.objects.filter(id=id_livro).exists()
                if livro_existe:
                    livro = Livro.objects.get(id=id_livro)
                    formulario_atualizar_livro = FormularioAtualizarLivro(
                        initial={
                            'isbn': livro.isbn,
                            'titulo': livro.titulo,
                            'resumo': livro.resumo,
                            'subtitulo': livro.subtitulo,
                            'lancamento': livro.lancamento,
                            'editora': livro.editora,
                            'copias': livro.copias,
                            'autores': livro.autores.all().values_list('id', flat=True),
                            'categoria': livro.categoria.id,
                        }
                    )
                    return render(request, template_name, context={'form': formulario_atualizar_livro, 'livro': livro, 'user_context': user_context})
            if request.method == 'POST':
                formulario_atualizar_livro = FormularioAtualizarLivro(request.POST)
                if formulario_atualizar_livro.is_valid():
                    livro = Livro.objects.get(id=id_livro)
                    livro.titulo = formulario_atualizar_livro.cleaned_data['titulo']
                    livro.resumo = formulario_atualizar_livro.cleaned_data['resumo']
                    livro.subtitulo = formulario_atualizar_livro.cleaned_data['subtitulo']
                    livro.lancamento = formulario_atualizar_livro.cleaned_data['lancamento']
                    livro.editora = formulario_atualizar_livro.cleaned_data['editora']
                    livro.copias = formulario_atualizar_livro.cleaned_data['copias']
                    livro.categoria = Categoria.objects.get(id=formulario_atualizar_livro.cleaned_data['categoria'])
                    livro.autores.set(formulario_atualizar_livro.cleaned_data['autores'])
                    livro.save()
                    messages.add_message(request, messages.SUCCESS, 'Livro atualizado com sucesso.')
                    return redirect('livro:detalhar_livro', id_livro=livro.id)
                else:
                    pprint(formulario_atualizar_livro.errors)
                    messages.add_message(request, messages.ERROR, 'Erro ao atualizar o livro. Verifique os dados informados.')
                    livro = Livro.objects.get(id=id_livro)
                    return render(request, template_name, context={'form': formulario_atualizar_livro, 'livro': livro, 'user_context': user_context})
        else:
            messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não está autenticado.')
        return redirect('usuario:entrar')

def deletar_livro(request:HttpRequest, id_livro:int) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            livro_existe = Livro.objects.filter(id=id_livro).exists()
            if livro_existe:
                livro = Livro.objects.get(id=id_livro)
                livro.delete()
                messages.add_message(request, messages.SUCCESS, 'Livro deletado com sucesso.')
                pagina_anterior = request.META.get('HTTP_REFERER')
                return redirect(pagina_anterior)
            else:
                messages.add_message(request, messages.ERROR, 'Livro não encontrado.')
                pagina_anterior = request.META.get('HTTP_REFERER')
                return redirect(pagina_anterior)
        else:
            messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não está autenticado.')
        return redirect('usuario:entrar')

# Implementação de Emprestimo e Reserva de Livros
def reservar_livro(request:HttpRequest, id_livro:int, usuario:str) -> HttpResponse:
    return HttpResponse("View reservar livro")

# CRUD para Autor

def criar_autor(request:HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            if request.method == 'GET':
                template_name = "livro/criar_autor.html"
                formulario_autor = FormularioAutor()
                return render(request, template_name, context={'form': formulario_autor, 'user_context': user_context})
            if request.method == 'POST':
                formulario_autor = FormularioAutor(request.POST)
                if formulario_autor.is_valid():
                    nome = formulario_autor.cleaned_data['nome']
                    sobrenome = formulario_autor.cleaned_data['sobrenome']
                    email_de_contato = formulario_autor.cleaned_data['email_de_contato']
                    nascimento = formulario_autor.cleaned_data['nascimento']
                    sexo = formulario_autor.cleaned_data['sexo']
                    nacionalidade = formulario_autor.cleaned_data['nacionalidade']
                    novo_autor = Autor.objects.create(
                        nome=nome,
                        sobrenome=sobrenome,
                        email_de_contato=email_de_contato,
                        nascimento=nascimento,
                        sexo=sexo,
                        nacionalidade=nacionalidade
                    )
                    novo_autor.save()
                    messages.add_message(request, messages.SUCCESS, 'Autor criado com sucesso.')
                    return redirect('livro:listar_autores')
                else:
                    messages.add_message(request, messages.ERROR, 'Erro ao criar o autor. Verifique os dados informados.')
                    template_name = "livro/criar_autor.html"
                    return render(request, template_name, context={'form': formulario_autor, 'user_context': user_context})
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
        return redirect('usuario:entrar')

def detalhar_autor(request:HttpRequest, id_autor:int) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            autor_existe = Autor.objects.filter(id=id_autor).exists()
            if autor_existe:
                autor = Autor.objects.get(id=id_autor)
                template_name = "livro/detalhar_autor.html"
                return render(request, template_name, context={'autor':autor, 'user_context': user_context})
            else:
                messages.add_message(request, messages.ERROR, 'Autor não encontrado.')
                return redirect('livro:listar_autores')
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def atualizar_autor(request:HttpRequest, id_autor:int) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                        'aluno': user_is_aluno(request.user),
                        'professor': user_is_professor(request.user),
                        'funcionario': user_is_funcionario(request.user),
            }
            template_name = "livro/atualizar_autor.html"
            if request.method == 'GET':
                autor_existe = Autor.objects.filter(id=id_autor).exists()
                if autor_existe:
                    autor = Autor.objects.get(id=id_autor)
                    formulario_atualizar_autor = FormularioAtualizarAutor(
                        initial={
                            'nome': autor.nome,
                            'sobrenome': autor.sobrenome,
                            'email_de_contato': autor.email_de_contato,
                            'nascimento': autor.nascimento,
                            'sexo': autor.sexo,
                            'nacionalidade': autor.nacionalidade,
                        }
                    )
                    return render(request, template_name, context={'form': formulario_atualizar_autor, 'user_context': user_context, 'autor': autor})
                else:
                    messages.add_message(request, messages.ERROR, 'Autor não encontrado.')
                    return redirect('livro:listar_autores')
            if request.method == 'POST':
                formulario_atualizar_autor = FormularioAtualizarAutor(request.POST)
                if formulario_atualizar_autor.is_valid():
                    autor = Autor.objects.get(id=id_autor)
                    autor.nome = formulario_atualizar_autor.cleaned_data['nome']
                    autor.sobrenome = formulario_atualizar_autor.cleaned_data['sobrenome']
                    autor.email_de_contato = formulario_atualizar_autor.cleaned_data['email_de_contato']
                    autor.nascimento = formulario_atualizar_autor.cleaned_data['nascimento']
                    autor.sexo = formulario_atualizar_autor.cleaned_data['sexo']
                    autor.nacionalidade = formulario_atualizar_autor.cleaned_data['nacionalidade']
                    autor.save()
                    messages.add_message(request, messages.SUCCESS, 'Autor atualizado com sucesso.')
                    return redirect('livro:detalhar_autor', id_autor=autor.id)
                else:
                    pprint(formulario_atualizar_autor.errors)
                    messages.add_message(request, messages.ERROR, 'Erro ao atualizar o autor. Verifique os dados informados.')
                    autor = Autor.objects.get(id=id_autor)
                    return render(request, template_name, context={'form': formulario_atualizar_autor, 'autor': autor, 'user_context': user_context})
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def deletar_autor(request:HttpRequest, id_autor:int) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            autor_existe = Autor.objects.filter(id=id_autor).exists()
            if autor_existe:
                autor = Autor.objects.get(id=id_autor)
                autor.delete()
                messages.add_message(request, messages.SUCCESS, 'Autor deletado com sucesso.')
                pagina_anterior = request.META.get('HTTP_REFERER')
                return redirect(pagina_anterior)
            else:
                messages.add_message(request, messages.ERROR, 'Autor não encontrado.')
                pagina_anterior = request.META.get('HTTP_REFERER')
                return redirect(pagina_anterior)
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

# CRUD para Categoria
def criar_categoria(request:HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            if request.method == 'GET':
                template_name = "livro/criar_categoria.html"
                formulario_categoria = FormularioCategoria()
                return render(request, template_name, context={'form': formulario_categoria, 'user_context': user_context})
            if request.method == 'POST':
                formulario_categoria = FormularioCategoria(request.POST)
                if formulario_categoria.is_valid():
                    categoria = formulario_categoria.cleaned_data['categoria']
                    descricao = formulario_categoria.cleaned_data['descricao']
                    nova_categoria = Categoria.objects.create(
                        categoria=categoria,
                        descricao=descricao
                    )
                    nova_categoria.save()
                    messages.add_message(request, messages.SUCCESS, 'Categoria criada com sucesso.')
                    return redirect('livro:listar_categorias')
                else:
                    messages.add_message(request, messages.ERROR, 'Erro ao criar a categoria. Verifique os dados informados.')
                    template_name = "livro/criar_categoria.html"
                    return render(request, template_name, context={'form': formulario_categoria, 'user_context': user_context})
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def detalhar_categoria(request:HttpRequest, id_categoria:int) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            categoria_existe = Categoria.objects.filter(id=id_categoria).exists()
            if categoria_existe:
                categoria = Categoria.objects.get(id=id_categoria)
                livros_categoria = Livro.objects.filter(categoria = categoria)
                contador_livros = len(livros_categoria)
                detalhes = {
                    'livros': livros_categoria,
                    'contador_livros': contador_livros,
                }
                template_name = "livro/detalhar_categoria.html"
                return render(request, template_name, context={'categoria':categoria, 'user_context': user_context, 'detalhes': detalhes})
            else:
                messages.add_message(request, messages.ERROR, 'Categoria não encontrada.')
                return redirect('livro:listar_categorias')
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def atualizar_categoria(request:HttpRequest, id_categoria:int) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            template_name = "livro/atualizar_categoria.html"
            if request.method == 'GET':
                categoria_existe = Categoria.objects.filter(id=id_categoria).exists()
                if categoria_existe:
                    categoria = Categoria.objects.get(id=id_categoria)
                    formulario_atualizar_categoria = FormularioAtualizarCategoria(
                        initial={
                            'categoria': categoria.categoria,
                            'descricao': categoria.descricao,
                        }
                    )
                    return render(request, template_name, context={'form': formulario_atualizar_categoria, 'user_context': user_context, 'categoria': categoria})
            if request.method == 'POST':
                formulario_atualizar_categoria = FormularioAtualizarCategoria(request.POST)
                if formulario_atualizar_categoria.is_valid():
                    categoria = Categoria.objects.get(id=id_categoria)
                    categoria.categoria = formulario_atualizar_categoria.cleaned_data['categoria']
                    categoria.descricao = formulario_atualizar_categoria.cleaned_data['descricao']
                    categoria.save()
                    messages.add_message(request, messages.SUCCESS, 'Categoria atualizada com sucesso.')
                    return redirect('livro:detalhar_categoria', id_categoria=categoria.id)
                else:
                    pprint(formulario_atualizar_categoria.errors)
                    messages.add_message(request, messages.ERROR, 'Erro ao atualizar a categoria. Verifique os dados informados.')
                    categoria = Categoria.objects.get(id=id_categoria)
                    return render(request, template_name, context={'form': formulario_atualizar_categoria, 'categoria': categoria, 'user_context': user_context})
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def deletar_categoria(request:HttpRequest, id_categoria:int) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            categoria_existe = Categoria.objects.filter(id=id_categoria).exists()
            if categoria_existe:
                categoria = Categoria.objects.get(id=id_categoria)
                categoria.delete()
                messages.add_message(request, messages.SUCCESS, 'Categoria deletada com sucesso.')
                pagina_anterior = request.META.get('HTTP_REFERER')
                return redirect(pagina_anterior)
            else:
                messages.add_message(request, messages.ERROR, 'Categoria não encontrada.')
                pagina_anterior = request.META.get('HTTP_REFERER')
                return redirect(pagina_anterior)
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')


# Views de Reserva

def criar_reserva(request: HttpRequest, id_livro:int):
    if request.user.is_authenticated:
        if user_is_aluno(request.user):
            return criar_reserva_aluno(request, id_livro)
        elif user_is_professor(request.user):
            return criar_reserva_professor(request, id_livro)
        elif user_is_funcionario(request.user):
            return criar_reserva_funcionario(request, id_livro)
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é aluno, professor ou funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def listar_reservas(request:HttpRequest):
    if request.user.is_authenticated:
        user_context = {
            'aluno': user_is_aluno(request.user),
            'professor': user_is_professor(request.user),
            'funcionario': user_is_funcionario(request.user),
        }
        reservas = Reserva.objects.filter(usuario=request.user).exists()
        template_name = "livro/listar_reservas.html"
        if reservas:
            reservas = Reserva.objects.filter(usuario=request.user)
            return render(request, template_name=template_name, context={'reservas':reservas, 'user_context': user_context})
        else:
            messages.add_message(request, messages.ERROR, 'Não existem reservas para este usuário.')
            return render(request, template_name, context={'reserva':True, 'user_context': user_context})
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def listar_todas_reservas(request:HttpRequest):
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            reservas = Reserva.objects.all().exists()
            template_name = "livro/listar_todas_reservas.html"
            if reservas:
                reservas = Reserva.objects.all().order_by('-data_reserva')
                return render(request, template_name=template_name, context={'reservas':reservas, 'user_context': user_context})
            else:
                messages.add_message(request, messages.ERROR, 'Não existem reservas na biblioteca.')
                return render(request, template_name, context={'reserva':True})
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def ler_reserva(request: HttpRequest, id_reserva:int) -> HttpResponse:
    if request.user.is_authenticated:
        reserva = Reserva.objects.filter(id=id_reserva).exists()
        if reserva:
            template_name = "livro/detalhe_reserva.html"
            reserva = Reserva.objects.get(id=id_reserva)
            return render(request, template_name=template_name, context={'reserva': reserva})
        else:
            messages.add_message(request, messages.ERROR, f'reserva nao encontrada.')
            return redirect('livro:listar_reservas')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def atualizar_reserva(request: HttpRequest, id_reserva:int) -> HttpResponse:
    # Nao deve ser usada ja que a logica de cada reserva impossibilita que os 
    # dados sejam alterados
    return HttpResponse('View de atualizar reserva')

def deletar_reserva(request: HttpRequest, id_reserva:int) -> HttpResponse:
    if request.user.is_authenticated:
        reserva = Reserva.objects.filter(id=id_reserva).exists()
        if reserva:
            reserva = Reserva.objects.get(id=id_reserva)
            reserva.delete()
            messages.add_message(request, messages.SUCCESS, 'Reserva deletada com sucesso.')
            pagina_anterior = request.META.get('HTTP_REFERER')
            return redirect(pagina_anterior)
        else:
            messages.add_message(request, messages.ERROR, 'Reserva não encontrada.')
            pagina_anterior = request.META.get('HTTP_REFERER')
            return redirect(pagina_anterior)
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

# Views de Emprestimo

def criar_emprestimo(request: HttpRequest, id_livro:int, id_usuario:int):
    usuario = request.user  # O usuário deve ser um funcionario. Ele pode emprestar livros 
                            # para outros funcionarios, para si mesmo e para alunos e professores
    if usuario.is_authenticated and user_is_funcionario(usuario):
        # O proximo passo é identificar se o usuario que quer fazer o emprestimo eh
        # professor, aluno ou outro funcionario
        pass

def listar_emprestimos(request: HttpRequest):
    if request.user.is_authenticated:
        user_context = {
            'aluno': user_is_aluno(request.user),
            'professor': user_is_professor(request.user),
            'funcionario': user_is_funcionario(request.user),
        }
        emprestimos_existem = Emprestimo.objects.filter(usuario=request.user, ativo=True).exists()
        template_name = 'livro/listar_emprestimos.html'
        if emprestimos_existem:
            emprestimos = Emprestimo.objects.filter(usuario=request.user, ativo=True)
            return render(request, template_name, context={'emprestimos': emprestimos, 'user_context': user_context})
        else:
            messages.add_message(request, messages.ERROR, 'Não existem emprestimos para este usuário.')
            return render(request, template_name, context={'emprestimo':True, 'user_context': user_context})
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def ler_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    return HttpResponse('Views de ler emprestimo')

def atualizar_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    return HttpResponse('View de atualizar emprestimo')

def deletar_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            emprestimo = Emprestimo.objects.filter(id=id_emprestimo, ativo=True).exists()
            if emprestimo:
                emprestimo = Emprestimo.objects.get(id=id_emprestimo, ativo=True)
                emprestimo.ativo = False
                emprestimo.save()
                livro = emprestimo.livro
                livro.copias += 1
                livro.save()
                messages.add_message(request, messages.SUCCESS, 'Empréstimo finalizado com sucesso.')
                pagina_anterior = request.META.get('HTTP_REFERER')
                return redirect(pagina_anterior)
            else:
                messages.add_message(request, messages.ERROR, 'Empréstimo não encontrado ou já devolvido.')
                pagina_anterior = request.META.get('HTTP_REFERER')
                return redirect(pagina_anterior)
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')

def renovar_emprestimo(request: HttpRequest):
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            template_name = 'livro/renovar_emprestimo.html'
            if request.method == 'GET':
                formulario = FormularioRenovarEmprestimo()
                return render(request, template_name, context={'form': formulario, 'user_context': user_context})
            if request.method == 'POST':
                formulario = FormularioRenovarEmprestimo(request.POST)
                if formulario.is_valid():
                    usuario = formulario.cleaned_data['usuario']
                    emprestimos = Emprestimo.objects.filter(usuario__id=usuario, ativo=True).exists()
                    if emprestimos:
                        emprestimos = Emprestimo.objects.filter(usuario__id=usuario, ativo=True)
                        return render(request, template_name, context={'emprestimos': emprestimos, 'form': formulario, 'user_context': user_context})
                    else:
                        return render(request, template_name, context={'form': formulario, 'user_context': user_context})
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')


def renovar_emprestimo_aluno(usuario, livro):
    try:
        emprestimo = Emprestimo.objects.get(usuario=usuario, livro=livro, ativo=True)
        nova_data_devolucao = emprestimo.data_devolucao + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS['aluno'])
        # TODO: Adicionar checagens de quantas vezes o aluno ja renovou determinado emprestimo
        emprestimo.data_devolucao = nova_data_devolucao
        emprestimo.save()
        return True
    except:
        return False

def renovar_emprestimo_aluno(emprestimo):
    if emprestimo.numero_renovacoes < NUMERO_MAXIMO_DE_RENOVACOES_POR_USUARIO['aluno']:
        nova_data_devolucao = emprestimo.data_devolucao + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS['aluno'])
        emprestimo.data_devolucao = nova_data_devolucao
        emprestimo.numero_renovacoes += 1
        emprestimo.save()
        return True
    return False

def renovar_emprestimo_professor(emprestimo):
    if emprestimo.numero_renovacoes < NUMERO_MAXIMO_DE_RENOVACOES_POR_USUARIO['professor']:
        nova_data_devolucao = emprestimo.data_devolucao + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS['professor'])
        emprestimo.data_devolucao = nova_data_devolucao
        emprestimo.numero_renovacoes += 1
        emprestimo.save()
        return True
    return False

def renovar_emprestimo_funcionario(emprestimo):
    if emprestimo.numero_renovacoes < NUMERO_MAXIMO_DE_RENOVACOES_POR_USUARIO['funcionario']:
        nova_data_devolucao = emprestimo.data_devolucao + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS['funcionario'])
        emprestimo.data_devolucao = nova_data_devolucao
        emprestimo.numero_renovacoes += 1
        emprestimo.save()
        return True
    return False

def renovar_emprestimo_livro(request, emprestimo_id):
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            emprestimo = Emprestimo.objects.filter(id=emprestimo_id, ativo=True).exists()
            if emprestimo:
                emprestimo = Emprestimo.objects.get(id=emprestimo_id, ativo=True)
                usuario = emprestimo.usuario
                livro = emprestimo.livro
                if user_is_aluno(usuario.id):
                    renovou = renovar_emprestimo_aluno(emprestimo)
                    if renovou:
                        messages.add_message(request, messages.SUCCESS, 'Empréstimo renovado com sucesso para o aluno.')
                    else:
                        messages.add_message(request, messages.ERROR, 'Erro ao renovar o empréstimo para o aluno.')
                    pagina_anterior = request.META.get('HTTP_REFERER')
                    return redirect(pagina_anterior)
                if user_is_professor(usuario.id):
                    renovou = renovar_emprestimo_professor(emprestimo)
                    if renovou:
                        messages.add_message(request, messages.SUCCESS, 'Empréstimo renovado com sucesso para o professor.')
                    else:
                        messages.add_message(request, messages.ERROR, 'Erro ao renovar o empréstimo para o professor.')
                    pagina_anterior = request.META.get('HTTP_REFERER')
                    return redirect(pagina_anterior)
                if user_is_funcionario(usuario.id):
                    renovou = renovar_emprestimo_funcionario(emprestimo)
                    if renovou:
                        messages.add_message(request, messages.SUCCESS, 'Empréstimo renovado com sucesso para o funcionário.')
                    else:
                        messages.add_message(request, messages.ERROR, 'Erro ao renovar o empréstimo para o funcionário.')
                    pagina_anterior = request.META.get('HTTP_REFERER')
                    return redirect(pagina_anterior)
            else:
                messages.add_message(request, messages.ERROR, 'Empréstimo não encontrado ou já devolvido.')
                pagina_anterior = request.META.get('HTTP_REFERER')
                return redirect(pagina_anterior)
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

# TODO: Implementar view de historico de emprestimos

def historico_emprestimos(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if request.method == 'GET':
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            template_name = 'livro/historico_emprestimos.html'
            emprestimos_existem = Emprestimo.objects.all().exists()
            if emprestimos_existem:
                emprestimos = Emprestimo.objects.all().order_by('-data_emprestimo')
                return render(request, template_name, context={'emprestimos': emprestimos, 'user_context': user_context})
            else:
                messages.add_message(request, messages.ERROR, 'Não existe nenhum emprestimo ate o momento.')
                return render(request, template_name, context={'historico_emprestimo':True, 'user_context': user_context})
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

# Funcoes auxiliares para emprestimo de livros.
# TODO: Mover estas funcoes para utils.py
def checa_se_aluno_tem_numero_maximo_de_emprestimos(usuario_id:int) -> bool:
    aluno = Aluno.objects.get(usuario__id=usuario_id)
    if aluno.emprestimos <= MAX_EMPRESTIMOS_POR_USUARIO['aluno']:
        return False
    return True

def checa_se_professor_tem_numero_maximo_de_emprestimos(usuario_id:int) -> bool:
    professor = Professor.objects.get(usuario__id=usuario_id)
    if professor.emprestimos <= MAX_EMPRESTIMOS_POR_USUARIO['professor']:
        return False
    return True

def checa_se_funcionario_tem_numero_maximo_de_emprestimos(usuario_id:int) -> bool:
    funcionario = Funcionario.objects.get(usuario__id=usuario_id)
    if funcionario.emprestimos <= MAX_EMPRESTIMOS_POR_USUARIO['funcionario']:
        return False
    return True

def fazer_emprestimo(usuario, livro, data_emprestimo, data_devolucao):
    usuario = User.objects.get(id=usuario)
    livro = Livro.objects.get(id=livro)
    livro.copias -= 1
    livro.save()
    emprestimo = Emprestimo.objects.create(
        usuario=usuario,
        livro=livro,
        data_emprestimo=data_emprestimo,
        data_devolucao=data_devolucao,
        ativo=True
    )
    emprestimo.save()
    return True

# Fim das funcoes auxiliares para emprestimo de livros.

def emprestar_livro(request:HttpResponse) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            if request.method == 'GET':
                template_name = 'livro/emprestar_livro.html'
                formulario_emprestimo = FormularioCriarEmprestimo()
                limpar_mensagens(request)
                return render(request, template_name, context={'form': formulario_emprestimo, 'user_context': user_context})
            if request.method == 'POST':
                formulario_emprestimo = FormularioCriarEmprestimo(request.POST)
                if formulario_emprestimo.is_valid():
                    usuario_id = int(formulario_emprestimo.cleaned_data['usuario'])
                    livro_id = int(formulario_emprestimo.cleaned_data['livro'])
                    data_emprestimo = formulario_emprestimo.cleaned_data['data_emprestimo']
                    data_devolucao = data_emprestimo + timedelta(days=7)  # Empréstimo padrão de 7 dias
                    if user_is_aluno(usuario_id):
                        if not checa_se_aluno_tem_numero_maximo_de_emprestimos(usuario_id):
                            data_devolucao = data_emprestimo + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS['aluno'])
                            sucesso = fazer_emprestimo(usuario_id, livro_id, data_emprestimo, data_devolucao)
                            if sucesso:
                                messages.add_message(request, messages.SUCCESS, f'Empréstimo realizado com sucesso para o aluno. Data de devolução: {data_devolucao}.')
                                return redirect('livro:emprestar_livro')
                            else:
                                messages.add_message(request, messages.ERROR, f'Erro ao realizar o empréstimo para o aluno.')
                                return redirect('livro:emprestar_livro')
                        else:
                            messages.add_message(request, messages.ERROR, f'O aluno atingiu o número máximo de empréstimos.')
                            return redirect('livro:emprestar_livro')
                    if user_is_professor(usuario_id):
                        if not checa_se_professor_tem_numero_maximo_de_emprestimos(usuario_id):
                            data_devolucao = data_emprestimo + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS['professor'])
                            sucesso = fazer_emprestimo(usuario_id, livro_id, data_emprestimo, data_devolucao)
                            if sucesso:
                                messages.add_message(request, messages.SUCCESS, f'Empréstimo realizado com sucesso para o professor. Data de devolução: {data_devolucao}.')
                                return redirect('livro:emprestar_livro')
                            else:
                                messages.add_message(request, messages.ERROR, f'Erro ao realizar o empréstimo para o professor.')
                                return redirect('livro:emprestar_livro')
                        else:
                            messages.add_message(request, messages.ERROR, f'O professor atingiu o número máximo de empréstimos.')
                            return redirect('livro:emprestar_livro')
                    if user_is_funcionario(usuario_id):
                        if not checa_se_funcionario_tem_numero_maximo_de_emprestimos(usuario_id):
                            data_devolucao = data_emprestimo + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS['funcionario'])
                            sucesso = fazer_emprestimo(usuario_id, livro_id, data_emprestimo, data_devolucao)
                            if sucesso:
                                messages.add_message(request, messages.SUCCESS, f'Empréstimo realizado com sucesso para o funcionário. Data de devolução: {data_devolucao}.')
                                return redirect('livro:emprestar_livro')
                            else:
                                messages.add_message(request, messages.ERROR, f'Erro ao realizar o empréstimo para o funcionário.')
                                return redirect('livro:emprestar_livro')
                        else:
                            messages.add_message(request, messages.ERROR, f'O funcionário atingiu o número máximo de empréstimos.')
                            return redirect('livro:emprestar_livro')
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def devolver_livro(request, emprestimo_id):
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            emprestimo_existe = Emprestimo.objects.filter(id=emprestimo_id, ativo=True).exists()
            if emprestimo_existe:
                emprestimo = Emprestimo.objects.get(id=emprestimo_id, ativo=True)
                emprestimo.ativo = False
                emprestimo.save()
                livro = emprestimo.livro
                livro.copias += 1
                livro.save()
                messages.add_message(request, messages.SUCCESS, 'Livro devolvido com sucesso.')
                pagina_anterior = request.META.get('HTTP_REFERER')
                return redirect(pagina_anterior)
            else:
                messages.add_message(request, messages.ERROR, 'Empréstimo não encontrado ou já devolvido.')
                pagina_anterior = request.META.get('HTTP_REFERER')
                return redirect(pagina_anterior)
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def registrar_devolucao_livro(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            if request.method == 'GET':
                template_name = 'livro/registrar_devolucao.html'
                formulario_devolucao = FormularioRegistrarDevolucao()
                return render(request, template_name, context={'form': formulario_devolucao, 'user_context': user_context})
            if request.method == 'POST':
                formulario = FormularioRegistrarDevolucao(request.POST)
                if formulario.is_valid():
                    usuario_id = int(formulario.cleaned_data['usuario'])
                    emprestimos_existem = Emprestimo.objects.filter(usuario__id=usuario_id, ativo=True).exists()
                    if emprestimos_existem:
                        emprestimos = Emprestimo.objects.filter(usuario__id=usuario_id, ativo=True)
                        return render(request, 'livro/registrar_devolucao.html', context={'emprestimos': emprestimos, 'form': formulario, 'user_context': user_context})
                    else:
                        messages.add_message(request, messages.ERROR, 'Não existem empréstimos ativos para este usuário.')
                        return render(request, 'livro/registrar_devolucao.html', context={'form': formulario, 'user_context': user_context})
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')

def emprestar_livro_reserva(request, reserva_id):
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            reserva_existe = Reserva.objects.filter(id=reserva_id).exists()
            if reserva_existe:
                reserva = Reserva.objects.get(id=reserva_id)
                usuario = reserva.usuario
                livro = reserva.livro
                data_emprestimo = date.today()
                if user_is_aluno(usuario.id):
                    data_devolucao = data_emprestimo + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS['aluno'])
                    sucesso = fazer_emprestimo(usuario.id, livro.id, data_emprestimo, data_devolucao)
                    if sucesso:
                        reserva.delete()
                        messages.add_message(request, messages.SUCCESS, f'Empréstimo realizado com sucesso para o aluno. Data de devolução: {data_devolucao}.')
                        pagina_anterior = request.META.get('HTTP_REFERER')
                        return redirect(pagina_anterior)
                    else:
                        messages.add_message(request, messages.ERROR, f'Erro ao realizar o empréstimo para o aluno.')
                        pagina_anterior = request.META.get('HTTP_REFERER')
                        return redirect(pagina_anterior)
                if user_is_professor(usuario.id):
                    data_devolucao = data_emprestimo + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS['professor'])
                    sucesso = fazer_emprestimo(usuario.id, livro.id, data_emprestimo, data_devolucao)
                    if sucesso:
                        reserva.delete()
                        messages.add_message(request, messages.SUCCESS, f'Empréstimo realizado com sucesso para o professor. Data de devolução: {data_devolucao}.')
                        pagina_anterior = request.META.get('HTTP_REFERER')
                        return redirect(pagina_anterior)
                    else:
                        messages.add_message(request, messages.ERROR, f'Erro ao realizar o empréstimo para o professor.')
                        pagina_anterior = request.META.get('HTTP_REFERER')
                        return redirect(pagina_anterior)
                if user_is_funcionario(usuario.id):
                    data_devolucao = data_emprestimo + timedelta(days=NUM_MAX_DIAS_EMPRESTIMOS['funcionario'])
                    sucesso = fazer_emprestimo(usuario.id, livro.id, data_emprestimo, data_devolucao)
                    if sucesso:
                        reserva.delete()
                        messages.add_message(request, messages.SUCCESS, f'Empréstimo realizado com sucesso para o funcionário. Data de devolução: {data_devolucao}.')
                        pagina_anterior = request.META.get('HTTP_REFERER')
                        return redirect(pagina_anterior)
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def cancelar_reserva(request):
    if request.user.is_authenticated:
        if user_is_funcionario(request.user):
            user_context = {
                'aluno': user_is_aluno(request.user),
                'professor': user_is_professor(request.user),
                'funcionario': user_is_funcionario(request.user),
            }
            template_name = 'livro/cancelar_reserva.html'
            if request.method == 'GET':
                formulario_cancelar = FormularioCancelarReserva()
                return render(request, template_name, context={'form': formulario_cancelar, 'user_context': user_context})
            if request.method == 'POST':
                formulario = FormularioCancelarReserva(request.POST)
                if formulario.is_valid():
                    usuario_id = int(formulario.cleaned_data['usuario'])
                    reservas_existem = Reserva.objects.filter(usuario__id=usuario_id).exists()
                    if reservas_existem:
                        reservas = Reserva.objects.filter(usuario__id=usuario_id)
                        return render(request, template_name, context={'reservas': reservas, 'form': formulario, 'user_context': user_context})
                    else:
                        messages.add_message(request, messages.ERROR, 'Não existem reservas para este usuário.')
                        return render(request, template_name, context={'form': formulario, 'user_context': user_context})
        else:
            messages.add_message(request, messages.ERROR, f'Usuário não é funcionário.')
            return redirect('usuario:entrar')
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')