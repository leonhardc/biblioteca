from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.core.paginator import Paginator
# from django.contrib.auth.decorators import entrar_required
from .models import Livro
from datetime import date
from utils.utils import *
from django.db.models import Q
from usuario.constants import MAX_RESERVAS_POR_USUARIO
from utils.usuarios.utils import user_is_aluno, user_is_professor, user_is_funcionario
from utils.livros.utils import criar_reserva_aluno, criar_reserva_professor, criar_reserva_funcionario

# Método de Listar Livros, Autores e Categorias
def listar_livros(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        template_name = "livro/livros.html"
        itens_por_pagina = 21
        termo_pesquisa = request.GET.get("pesquisa", "").strip()
        
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
        
        # Ordenação consistente (importante para paginação)
        livros_queryset = livros_queryset.order_by('-id')
        
        # Paginação otimizada
        paginator = Paginator(livros_queryset, itens_por_pagina)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)
        
        context = {
            "livros": page_obj,
            "termo_busca": termo_pesquisa,
            "total_resultados": paginator.count,
        }
        
        return render(request, template_name, context)
    else:
        messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não está autenticado.')
        return redirect('usuario:entrar')

def listar_autores(resquest: HttpRequest) -> HttpResponse:
    return HttpResponse('View listar autores')

def listar_categorias(request: HttpRequest) -> HttpResponse:
    return HttpResponse("View listar Categorias")

# Implementação do CRUD para livro
def criar_livro(request: HttpRequest) -> HttpResponse:
    return HttpResponse("View Criar Livro")

def detalhar_livro(request: HttpRequest, id_livro:int) -> HttpResponse:
    if request.user.is_authenticated:
        livro = Livro.objects.filter(id=id_livro).exists()
        if livro:
            livro = Livro.objects.get(id=id_livro)
            template_name = "livro/detalhar_livro.html"
            return render(request, template_name, context={'livro':livro})
        else:
            # TODO: IMPLEMENTAR LOGICA PARA MANDAR UMA MENSAGEM DE ERRO PARA O TEMPLATE ORIGINAL
            return HttpResponse('Livro não encontrado.')
    else:
        messages.add_message(request, messages.ERROR, 'Operação inválida. O usuário não está autenticado.')
        return redirect('usuario:entrar')

def atualizar_livro(request:HttpRequest, id_livro:int) -> HttpResponse:
    return HttpResponse("View Atualizar Livro")

def deletar_livro(request:HttpRequest, id_livro:int) -> HttpResponse:
    return HttpResponse("View Deletar Livro")

# Implementação de Emprestimo e Reserva de Livros
def reservar_livro(request:HttpRequest, id_livro:int, usuario:str) -> HttpResponse:
    return HttpResponse("View reservar livro")

def emprestar_livro(request:HttpResponse, id_livro:int, usuario:str) -> HttpResponse:
    return HttpResponse("View Emprestar Livro")

# CRUD para Autor
def criar_autor(request:HttpRequest) -> HttpResponse:
    return HttpResponse("View criar Autor")

def detalhar_autor(request:HttpRequest, id_autor:int) -> HttpResponse:
    return HttpResponse("View detalhar Autor")

def atualizar_autor(request:HttpRequest, id_autor:int) -> HttpResponse:
    return HttpResponse("View atualizar Autor")

def deletar_autor(request:HttpRequest, id_autor:int) -> HttpResponse:
    return HttpResponse("View deletar Autor")

# CRUD para Categoria
def criar_categoria(request:HttpRequest) -> HttpResponse:
    return HttpResponse("View criar Categoria")

def detalhar_categoria(request:HttpRequest, id_categoria:int) -> HttpResponse:
    return HttpResponse("View detalhar Categoria")

def atualizar_categoria(request:HttpRequest, id_categoria:int) -> HttpResponse:
    return HttpResponse("View atualizar Categoria")

def deletar_categoria(request:HttpRequest, id_categoria:int) -> HttpResponse:
    return HttpResponse("View deletar Categoria")


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
        reservas = Reserva.objects.filter(usuario=request.user).exists()
        template_name = "livro/listar_reservas.html"
        if reservas:
            reservas = Reserva.objects.filter(usuario=request.user)
            return render(request, template_name=template_name, context={'reservas':reservas})
        else:
            messages.add_message(request, messages.ERROR, 'Não existem reservas para este usuário.')
            return render(request, template_name, context={'reserva':True})
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def ler_reserva(request: HttpRequest, id_reserva:int) -> HttpResponse:
    if request.user.is_authenticated:
        reserva = Reserva.objects.filter(id=id_reserva).exists()
        if reserva:
            # TODO: Logica implementada, falta criar o template
            template_name = ""
            reserva = Reserva.objects.get(id=id_reserva)
            return render(request, template_name=template_name, context={})
        else:
            return HttpResponse("Reserva não encontrada.")
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
        emprestimos_existem = Emprestimo.objects.filter(usuario=request.user, ativo=True).exists()
        template_name = 'livro/listar_emprestimos.html'
        if emprestimos_existem:
            emprestimos = Emprestimo.objects.filter(usuario=request.user, ativo=True)
            return render(request, template_name, context={'emprestimos': emprestimos})
        else:
            messages.add_message(request, messages.ERROR, 'Não existem emprestimos para este usuário.')
            return render(request, template_name, context={'emprestimo':True})
    else:
        messages.add_message(request, messages.ERROR, f'Usuário não autenticado.')
        return redirect('usuario:entrar')

def ler_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    return HttpResponse('Views de ler emprestimo')

def atualizar_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    return HttpResponse('View de atualizar emprestimo')

def deletar_emprestimo(request: HttpRequest, id_emprestimo:int) -> HttpResponse:
    return HttpResponse('View de deletar emprestimo')