from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from usuario.models import Aluno, Professor, Funcionario
from curso.models import Curso
from livro.models import Emprestimo, Reserva, Livro
import datetime
from unittest.mock import patch, MagicMock
from django.http import HttpResponse


class AlunoViewsTestCase(TestCase):
    """Testes unitários para as views relacionadas aos Alunos"""

    def setUp(self):
        """Configuração inicial para todos os testes"""
        self.client = Client()
        
        # Criar um curso
        self.curso = Curso.objects.create(
            cod_curso='ENG001',
            curso='Engenharia de Software',
            descricao='Curso de Engenharia de Software',
            turno='M',
            duracao=5
        )
        
        # Criar usuário comum
        self.user = User.objects.create_user(
            username='aluno_teste',
            password='senha123',
            email='aluno@teste.com',
            first_name='João',
            last_name='Silva'
        )
        
        # Criar aluno
        self.aluno = Aluno.objects.create(
            usuario=self.user,
            matricula='123456',
            curso=self.curso,
            endereco='Rua Teste, 123',
            cpf='12345678901',
            ingresso=datetime.date.today(),
            conclusao_prevista=datetime.date.today() + datetime.timedelta(days=1825),
            ativo=True,
            reservas=0,
            emprestimos=0
        )
        
        # Criar usuário funcionário
        self.funcionario_user = User.objects.create_user(
            username='funcionario_teste',
            password='senha123',
            email='funcionario@teste.com',
            first_name='Maria',
            last_name='Santos'
        )
        
        self.funcionario = Funcionario.objects.create(
            usuario=self.funcionario_user,
            matricula='1001',
            cpf='98765432100',
            ativo=True,
            reservas=0,
            emprestimos=0
        )
        
        # Criar usuário admin
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@teste.com'
        )

    def test_listar_alunos_authenticated(self):
        """Testa listagem de alunos com usuário autenticado"""
        self.client.login(username='aluno_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(reverse('usuario:listar-alunos'))
            
            self.assertEqual(response.status_code, 200)
            mock_render.assert_called_once()

    def test_listar_alunos_not_authenticated(self):
        """Testa listagem de alunos sem autenticação"""
        response = self.client.get(
            reverse('usuario:listar-alunos'),
            HTTP_REFERER='/some-page/'
        )
        
        # Deve redirecionar porque não está autenticado
        self.assertEqual(response.status_code, 302)

    def test_dashboard_aluno_authenticated(self):
        """Testa dashboard do aluno com usuário autenticado"""
        self.client.login(username='aluno_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(reverse('usuario:dashboard_aluno'))
            
            self.assertEqual(response.status_code, 200)

    def test_dashboard_aluno_not_authenticated(self):
        """Testa dashboard do aluno sem autenticação"""
        response = self.client.get(
            reverse('usuario:dashboard_aluno'),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_pagina_inicial_aluno_authenticated(self):
        """Testa página inicial do aluno com usuário autenticado"""
        self.client.login(username='aluno_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:pagina_inicial_aluno', kwargs={'uid': self.user.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_pagina_inicial_aluno_not_authenticated(self):
        """Testa página inicial do aluno sem autenticação"""
        response = self.client.get(
            reverse('usuario:pagina_inicial_aluno', kwargs={'uid': self.user.id})
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('usuario:entrar'))

    def test_criar_aluno_get_authenticated(self):
        """Testa GET para criação de aluno com usuário autenticado"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(reverse('usuario:criar-aluno'))
            
            self.assertEqual(response.status_code, 200)

    def test_criar_aluno_not_authenticated(self):
        """Testa criação de aluno sem autenticação"""
        response = self.client.get(
            reverse('usuario:criar-aluno'),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    @patch('usuario.views.FormularioAluno')
    @patch('usuario.views.random.randint')
    def test_criar_aluno_post_success(self, mock_randint, mock_form):
        """Testa POST para criação de aluno com sucesso"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        # Mock do randint para gerar matricula
        mock_randint.return_value = 654321
        
        # Mock do formulário
        mock_form_instance = MagicMock()
        mock_form.return_value = mock_form_instance
        mock_form_instance.cleaned_data = {
            'nome': 'Pedro',
            'sobrenome': 'Costa',
            'email': 'pedro@teste.com',
            'usuario': 'pedro_costa',
            'cpf': '11122233344',
            'matricula': '654321',
            'curso': self.curso.id,
            'ingresso': datetime.date.today(),
            'conclusao_prevista': datetime.date.today() + datetime.timedelta(days=1825),
            'tipo_logradouro': 'Rua',
            'logradouro': 'Das Flores',
            'numero': '456',
            'bairro': 'Centro',
            'cep': '12345678',
            'cidade': 'São Paulo',
            'estado': 'SP',
            'complemento': 'Apto 10'
        }
        
        response = self.client.post(
            reverse('usuario:criar-aluno'),
            {},
            HTTP_REFERER='/some-page/'
        )
        
        # Verifica se há redirecionamento
        self.assertEqual(response.status_code, 302)

    def test_ler_aluno_authenticated(self):
        """Testa visualização de dados do próprio aluno autenticado"""
        self.client.login(username='aluno_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(reverse('usuario:ler-aluno'))
            
            self.assertEqual(response.status_code, 200)

    def test_ler_aluno_not_authenticated(self):
        """Testa visualização de dados do aluno sem autenticação"""
        response = self.client.get(
            reverse('usuario:ler-aluno'),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_detalhes_aluno_as_funcionario(self):
        """Testa visualização de detalhes do aluno como funcionário"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:detalhes-aluno', kwargs={'uid': self.aluno.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_detalhes_aluno_as_admin(self):
        """Testa visualização de detalhes do aluno como admin"""
        self.client.login(username='admin', password='admin123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:detalhes-aluno', kwargs={'uid': self.aluno.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_detalhes_aluno_as_aluno(self):
        """Testa visualização de detalhes do próprio aluno"""
        self.client.login(username='aluno_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:detalhes-aluno', kwargs={'uid': self.aluno.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_detalhes_aluno_not_authenticated(self):
        """Testa visualização de detalhes sem autenticação"""
        response = self.client.get(
            reverse('usuario:detalhes-aluno', kwargs={'uid': self.aluno.id}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_atualizar_aluno_get_as_funcionario(self):
        """Testa GET para atualização de aluno como funcionário"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:atualizar-aluno', kwargs={'uid': self.aluno.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_atualizar_aluno_get_as_admin(self):
        """Testa GET para atualização de aluno como admin"""
        self.client.login(username='admin', password='admin123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:atualizar-aluno', kwargs={'uid': self.aluno.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_atualizar_aluno_aluno_inexistente(self):
        """Testa atualização de aluno inexistente"""
        self.client.login(username='funcionario_teste', password='senha123')
        response = self.client.get(
            reverse('usuario:atualizar-aluno', kwargs={'uid': 99999}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_atualizar_aluno_not_authenticated(self):
        """Testa atualização de aluno sem autenticação"""
        response = self.client.get(
            reverse('usuario:atualizar-aluno', kwargs={'uid': self.aluno.id}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_deletar_aluno_authenticated(self):
        """Testa deleção de aluno com usuário autenticado"""
        # Criar um novo aluno para deletar
        novo_user = User.objects.create_user(
            username='aluno_deletar',
            password='senha123',
            email='deletar@teste.com'
        )
        novo_aluno = Aluno.objects.create(
            usuario=novo_user,
            matricula='999999',
            curso=self.curso,
            endereco='Rua Teste, 999',
            cpf='99999999999',
            ingresso=datetime.date.today(),
            conclusao_prevista=datetime.date.today() + datetime.timedelta(days=1825),
            ativo=True,
            reservas=0,
            emprestimos=0
        )
        
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('usuario:deletar-aluno', kwargs={'uid': novo_aluno.id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Aluno.objects.filter(id=novo_aluno.id).exists())

    def test_deletar_aluno_inexistente(self):
        """Testa deleção de aluno inexistente"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('usuario:deletar-aluno', kwargs={'uid': 99999}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_deletar_aluno_not_authenticated(self):
        """Testa deleção de aluno sem autenticação"""
        response = self.client.get(
            reverse('usuario:deletar-aluno', kwargs={'uid': self.aluno.id}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)


class AlunoUtilityFunctionsTestCase(TestCase):
    """Testes para funções utilitárias relacionadas aos alunos"""

    def setUp(self):
        """Configuração inicial para testes de funções utilitárias"""
        self.curso = Curso.objects.create(
            cod_curso='ENG001',
            curso='Engenharia de Software',
            descricao='Curso de Engenharia',
            turno='M',
            duracao=5
        )
        
        self.user = User.objects.create_user(
            username='aluno_util',
            password='senha123',
            email='util@teste.com'
        )
        
        self.aluno = Aluno.objects.create(
            usuario=self.user,
            matricula='111111',
            curso=self.curso,
            endereco='Rua Util, 111',
            cpf='11111111111',
            ingresso=datetime.date.today(),
            conclusao_prevista=datetime.date.today() + datetime.timedelta(days=1825),
            ativo=True,
            reservas=0,
            emprestimos=0
        )

    @patch('usuario.views.Reserva.objects.filter')
    def test_get_reservas_ativas_usuario(self, mock_filter):
        """Testa obtenção de reservas ativas do usuário"""
        from usuario.views import get_reservas_ativas_usuario
        
        mock_filter.return_value = []
        result = get_reservas_ativas_usuario(self.user)
        
        mock_filter.assert_called_once_with(usuario=self.user, ativo=True)

    @patch('usuario.views.Emprestimo.objects.filter')
    def test_get_emprestimos_ativos_usuario(self, mock_filter):
        """Testa obtenção de empréstimos ativos do usuário"""
        from usuario.views import get_emprestimos_ativos_usuario
        
        mock_filter.return_value = []
        result = get_emprestimos_ativos_usuario(self.user)
        
        mock_filter.assert_called_once_with(usuario=self.user, ativo=True)

    @patch('usuario.views.Emprestimo.objects.filter')
    def test_get_emprestimos_pendentes_usuario(self, mock_filter):
        """Testa obtenção de empréstimos pendentes do usuário"""
        from usuario.views import get_emprestimos_pendentes_usuario
        
        mock_filter.return_value = []
        result = get_emprestimos_pendentes_usuario(self.user)
        
        mock_filter.assert_called_once_with(usuario=self.user, ativo=True, pendente=True)


class AlunoPaginationTestCase(TestCase):
    """Testes para paginação na listagem de alunos"""

    def setUp(self):
        """Criar múltiplos alunos para testar paginação"""
        self.curso = Curso.objects.create(
            cod_curso='ENG001',
            curso='Engenharia de Software',
            descricao='Curso de Engenharia',
            turno='M',
            duracao=5
        )
        
        # Criar 25 alunos para testar paginação (20 por página)
        for i in range(25):
            user = User.objects.create_user(
                username=f'aluno_{i}',
                password='senha123',
                email=f'aluno{i}@teste.com'
            )
            Aluno.objects.create(
                usuario=user,
                matricula=f'{100000 + i}',
                curso=self.curso,
                endereco=f'Rua {i}',
                cpf=f'{10000000000 + i}',
                ingresso=datetime.date.today(),
                conclusao_prevista=datetime.date.today() + datetime.timedelta(days=1825),
                ativo=True,
                reservas=0,
                emprestimos=0
            )
        
        self.user = User.objects.create_user(
            username='user_auth',
            password='senha123'
        )

    def test_listar_alunos_primeira_pagina(self):
        """Testa primeira página da listagem de alunos"""
        self.client.login(username='user_auth', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(reverse('usuario:listar-alunos'))
            
            self.assertEqual(response.status_code, 200)

    def test_listar_alunos_segunda_pagina(self):
        """Testa segunda página da listagem de alunos"""
        self.client.login(username='user_auth', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(reverse('usuario:listar-alunos') + '?page=2')
            
            self.assertEqual(response.status_code, 200)


class ProfessorViewsTestCase(TestCase):
    """Testes unitários para as views relacionadas aos Professores"""

    def setUp(self):
        """Configuração inicial para todos os testes"""
        self.client = Client()
        
        # Criar um curso
        self.curso = Curso.objects.create(
            cod_curso='ENG001',
            curso='Engenharia de Software',
            descricao='Curso de Engenharia de Software',
            turno='M',
            duracao=5
        )
        
        # Criar usuário professor
        self.user = User.objects.create_user(
            username='professor_teste',
            password='senha123',
            email='professor@teste.com',
            first_name='Carlos',
            last_name='Oliveira'
        )
        
        # Criar professor
        self.professor = Professor.objects.create(
            usuario=self.user,
            matricula='P001',
            curso=self.curso,
            cpf='11111111111',
            regime='40h',
            contratacao=datetime.date.today(),
            ativo=True,
            reservas=0,
            emprestimos=0
        )
        
        # Criar usuário funcionário
        self.funcionario_user = User.objects.create_user(
            username='funcionario_teste',
            password='senha123',
            email='funcionario@teste.com',
            first_name='Maria',
            last_name='Santos'
        )
        
        self.funcionario = Funcionario.objects.create(
            usuario=self.funcionario_user,
            matricula='F001',
            cpf='22222222222',
            ativo=True,
            reservas=0,
            emprestimos=0
        )
        
        # Criar usuário admin
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@teste.com'
        )

    def test_pagina_inicial_professor_authenticated(self):
        """Testa página inicial do professor com usuário autenticado"""
        self.client.login(username='professor_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:pagina_inicial_professor', kwargs={'uid': self.user.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_pagina_inicial_professor_not_authenticated(self):
        """Testa página inicial do professor sem autenticação"""
        response = self.client.get(
            reverse('usuario:pagina_inicial_professor', kwargs={'uid': self.user.id})
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('usuario:entrar'))

    def test_criar_professor_get_authenticated(self):
        """Testa GET para criação de professor com usuário autenticado"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(reverse('usuario:criar-professor'))
            
            self.assertEqual(response.status_code, 200)

    def test_criar_professor_not_authenticated(self):
        """Testa criação de professor sem autenticação"""
        response = self.client.get(
            reverse('usuario:criar-professor'),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_ler_professor_authenticated(self):
        """Testa visualização de dados do professor autenticado"""
        self.client.login(username='professor_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:ler-professor', kwargs={'uid': self.professor.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_ler_professor_not_authenticated(self):
        """Testa visualização de dados do professor sem autenticação"""
        response = self.client.get(
            reverse('usuario:ler-professor', kwargs={'uid': self.professor.id}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_detalhes_professor_as_funcionario(self):
        """Testa visualização de detalhes do professor como funcionário"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:detalhes-professor', kwargs={'uid': self.professor.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_detalhes_professor_as_admin(self):
        """Testa visualização de detalhes do professor como admin"""
        self.client.login(username='admin', password='admin123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:detalhes-professor', kwargs={'uid': self.professor.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_atualizar_professor_get_as_funcionario(self):
        """Testa GET para atualização de professor como funcionário"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:atualizar-professor', kwargs={'uid': self.professor.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_atualizar_professor_get_as_admin(self):
        """Testa GET para atualização de professor como admin"""
        self.client.login(username='admin', password='admin123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:atualizar-professor', kwargs={'uid': self.professor.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_atualizar_professor_professor_inexistente(self):
        """Testa atualização de professor inexistente"""
        self.client.login(username='funcionario_teste', password='senha123')
        response = self.client.get(
            reverse('usuario:atualizar-professor', kwargs={'uid': 99999}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_atualizar_professor_not_authenticated(self):
        """Testa atualização de professor sem autenticação"""
        response = self.client.get(
            reverse('usuario:atualizar-professor', kwargs={'uid': self.professor.id}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_deletar_professor_authenticated(self):
        """Testa deleção de professor com usuário autenticado"""
        # Criar um novo professor para deletar
        novo_user = User.objects.create_user(
            username='professor_deletar',
            password='senha123',
            email='deletar@teste.com'
        )
        novo_professor = Professor.objects.create(
            usuario=novo_user,
            matricula='P999',
            curso=self.curso,
            cpf='99999999999',
            regime='20h',
            contratacao=datetime.date.today(),
            ativo=True,
            reservas=0,
            emprestimos=0
        )
        
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('usuario:deletar-professor', kwargs={'uid': novo_professor.id}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Professor.objects.filter(id=novo_professor.id).exists())

    def test_deletar_professor_inexistente(self):
        """Testa deleção de professor inexistente"""
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('usuario:deletar-professor', kwargs={'uid': 99999}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_deletar_professor_not_authenticated(self):
        """Testa deleção de professor sem autenticação"""
        response = self.client.get(
            reverse('usuario:deletar-professor', kwargs={'uid': self.professor.id}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)


class FuncionarioViewsTestCase(TestCase):
    """Testes unitários para as views relacionadas aos Funcionários"""

    def setUp(self):
        """Configuração inicial para todos os testes"""
        self.client = Client()
        
        # Criar usuário funcionário
        self.user = User.objects.create_user(
            username='funcionario_teste',
            password='senha123',
            email='funcionario@teste.com',
            first_name='Ana',
            last_name='Silva'
        )
        
        # Criar funcionário
        self.funcionario = Funcionario.objects.create(
            usuario=self.user,
            matricula='F001',
            cpf='33333333333',
            ativo=True,
            reservas=0,
            emprestimos=0
        )
        
        # Criar outro funcionário
        self.outro_funcionario_user = User.objects.create_user(
            username='outro_funcionario',
            password='senha123',
            email='outro@teste.com',
            first_name='Pedro',
            last_name='Costa'
        )
        
        self.outro_funcionario = Funcionario.objects.create(
            usuario=self.outro_funcionario_user,
            matricula='F002',
            cpf='44444444444',
            ativo=True,
            reservas=0,
            emprestimos=0
        )
        
        # Criar usuário admin
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@teste.com'
        )

    def test_pagina_inicial_funcionario_authenticated(self):
        """Testa página inicial do funcionário com usuário autenticado"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:pagina_inicial_funcionario', kwargs={'uid': self.user.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_pagina_inicial_funcionario_not_authenticated(self):
        """Testa página inicial do funcionário sem autenticação"""
        response = self.client.get(
            reverse('usuario:pagina_inicial_funcionario', kwargs={'uid': self.user.id})
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('usuario:entrar'))

    def test_criar_funcionario_get_authenticated(self):
        """Testa GET para criação de funcionário com usuário autenticado"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(reverse('usuario:criar-funcionario'))
            
            self.assertEqual(response.status_code, 200)

    def test_criar_funcionario_not_authenticated(self):
        """Testa criação de funcionário sem autenticação"""
        response = self.client.get(
            reverse('usuario:criar-funcionario'),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_ler_funcionario_authenticated(self):
        """Testa visualização de dados do funcionário autenticado"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:ler-funcionario', kwargs={'uid': self.funcionario.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_ler_funcionario_not_authenticated(self):
        """Testa visualização de dados do funcionário sem autenticação"""
        response = self.client.get(
            reverse('usuario:ler-funcionario', kwargs={'uid': self.funcionario.id}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_ler_funcionario_inexistente(self):
        """Testa visualização de funcionário inexistente"""
        self.client.login(username='funcionario_teste', password='senha123')
        response = self.client.get(
            reverse('usuario:ler-funcionario', kwargs={'uid': 99999}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_detalhes_funcionario_as_funcionario(self):
        """Testa visualização de detalhes do funcionário como funcionário"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:detalhes-funcionario', kwargs={'uid': self.funcionario.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_detalhes_funcionario_as_admin(self):
        """Testa visualização de detalhes do funcionário como admin"""
        self.client.login(username='admin', password='admin123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:detalhes-funcionario', kwargs={'uid': self.funcionario.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_atualizar_funcionario_get_as_funcionario(self):
        """Testa GET para atualização de funcionário como funcionário"""
        self.client.login(username='funcionario_teste', password='senha123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:atualizar-funcionario', kwargs={'uid': self.funcionario.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_atualizar_funcionario_get_as_admin(self):
        """Testa GET para atualização de funcionário como admin"""
        self.client.login(username='admin', password='admin123')
        
        with patch('usuario.views.render') as mock_render:
            mock_render.return_value = HttpResponse('OK')
            response = self.client.get(
                reverse('usuario:atualizar-funcionario', kwargs={'uid': self.funcionario.id})
            )
            
            self.assertEqual(response.status_code, 200)

    def test_atualizar_funcionario_not_authenticated(self):
        """Testa atualização de funcionário sem autenticação"""
        response = self.client.get(
            reverse('usuario:atualizar-funcionario', kwargs={'uid': self.funcionario.id}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)

    def test_deletar_funcionario_authenticated(self):
        """Testa deleção de funcionário com usuário autenticado"""
        # Criar um novo funcionário para deletar
        novo_user = User.objects.create_user(
            username='funcionario_deletar',
            password='senha123',
            email='deletar@teste.com'
        )
        novo_funcionario = Funcionario.objects.create(
            usuario=novo_user,
            matricula='F999',
            cpf='99999999999',
            ativo=True,
            reservas=0,
            emprestimos=0
        )
        
        self.client.login(username='admin', password='admin123')
        response = self.client.get(
            reverse('usuario:deletar-funcionario', kwargs={'uid': novo_funcionario.id}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Funcionario.objects.filter(id=novo_funcionario.id).exists())

    def test_deletar_funcionario_not_authenticated(self):
        """Testa deleção de funcionário sem autenticação"""
        response = self.client.get(
            reverse('usuario:deletar-funcionario', kwargs={'uid': self.funcionario.id}),
            HTTP_REFERER='/some-page/'
        )
        
        self.assertEqual(response.status_code, 302)
