# Biblioteca Universitária

> **📌 Nota sobre Contribuições:** Se suas contribuições para este projeto não estão aparecendo no seu perfil do GitHub, execute `./check-contributions.sh` ou consulte [CONTRIBUTING.md](CONTRIBUTING.md) para diagnóstico e soluções.

## 📋 Sobre o Projeto

Biblioteca Universitária é uma aplicação web para gerenciamento do acervo de livros de uma instituição de ensino fictícia. Desenvolvida em **Django** (framework Python para web), o projeto oferece um sistema completo de empréstimo e reserva de livros com suporte a múltiplos tipos de usuários.

Veja a aplicacão rodando em [biblioteca-academica](http://biblioteca.leonardorcosta.com)

### Credenciais de acesso

|Tipo de Usuario|Usuario|Senha|
|---------------|-------|-----|
|Aluno|	larissa_melo537|1234|
|Professor|bento_garcia129|1234|
|Funcionario|juan_alves305|1234|

### Contexto

Este projeto iniciou como trabalho final na disciplina de Banco de Dados durante o curso de Engenharia de Computação. Embora tenha inspiração naquele trabalho original, representa um desenvolvimento pessoal totalmente reestrutado, aplicando conhecimentos adquiridos desde então e implementando boas práticas modernas de desenvolvimento.

### Objetivo

Criar uma plataforma robusta para:
- Gerenciar o acervo de livros, autores e categorias
- Controlar empréstimos e reservas de livros
- Gerenciar diferentes tipos de usuários (alunos, professores, funcionários)
- Fornecer um painel administrativo completo
- Manter histórico de transações e operações

## 🏗️ Estrutura do Projeto

O projeto conta com 5 aplicações principais, cada uma com responsabilidades específicas:

```
biblioteca/                 # Configurações gerais da aplicação
├── settings.py             # Configuração de BD, apps, templates
├── urls.py                 # Roteamento principal
├── asgi.py
└── wsgi.py

administrador/              # Painel administrativo personalizado
├── models.py
├── views.py
├── urls.py
├── forms.py
├── admin.py
└── tests.py

usuario/                    # Gerenciamento de usuários (alunos, professores, funcionários)
├── models.py               # Models: Aluno, Professor, Funcionário
├── views.py                # Views e controladores
├── urls.py
├── forms.py
├── admin.py
└── tests.py

livro/                      # Gerenciamento de livros, autores, categorias
├── models.py               # Models: Livro, Autor, Categoria, Empréstimo, Reserva
├── views.py
├── urls.py
├── forms.py
├── admin.py
├── tests.py
├── signals/                # Sinais Django para operações automáticas
└── migrations/

curso/                      # Gerenciamento de cursos
├── models.py
├── views.py
├── urls.py
├── forms.py
├── admin.py
└── tests.py

notificacao/                # Sistema de notificações
├── models.py
├── views.py
└── urls.py

static/                     # Arquivos estáticos (CSS, JS, imagens)
templates/                  # Templates HTML
utils/                      # Utilitários e helpers
```

### App Biblioteca (Configuração Principal)

O app principal centraliza as configurações gerais da aplicação:

- **settings.py**: Configuração de banco de dados, apps instalados, templates, autenticação
- **urls.py**: Roteamento principal da aplicação
- **asgi.py e wsgi.py**: Configuração para deploy

### App Administrador

Um painel administrativo personalizado com funcionalidades completas:

- ✅ CRUD completo para todas as entidades
- ✅ Operações personalizadas em usuários, livros e cursos
- ✅ Controle granular de permissões
- ✅ Gerenciamento de empréstimos e reservas
- ✅ Visualização de histórico de transações

### App Usuário

Gerencia os três tipos principais de usuários do sistema:

#### 👤 Aluno
- Usuário mais populoso do sistema
- Pode visualizar seus dados pessoais
- Pode visualizar e filtrar livros disponíveis
- Pode reservar e alugar livros (quantidade limitada)
- Pode visualizar seus empréstimos e reservas ativas

#### 👨‍🏫 Professor
- Mesmas funcionalidades do aluno
- Limite maior de livros para empréstimo
- Prazo maior para devoluções

#### 👨‍💼 Funcionário
- Pode alugar livros para si e para outros usuários
- Pode visualizar e atualizar informações de livros
- Acesso a funcionalidades administrativas básicas
- Não pode alterar informações de outros usuários

**Modelos de Dados:**

```python
# Aluno
class Aluno(models.Model):
    usuario = models.ForeignKey(User, ...)
    matricula = models.CharField(...)
    curso = models.ForeignKey(Curso, ...)
    endereco = models.CharField(...)
    cpf = models.CharField(...)
    ingresso = models.DateField(...)
    conclusao_prevista = models.DateField(...)

# Professor
class Professor(models.Model):
    usuario = models.ForeignKey(User, ...)
    matricula = models.CharField(...)
    curso = models.ForeignKey(Curso, ...)
    cpf = models.CharField(...)
    regime = models.CharField(...)
    contratacao = models.DateField(...)

# Funcionário
class Funcionario(models.Model):
    usuario = models.ForeignKey(User, ...)
    matricula = models.CharField(...)
    cpf = models.CharField(...)
```

### App Livro

Núcleo do sistema, gerenciando toda a coleção:

- 📚 **Livros**: Título, ISBN, exemplares disponíveis, descrição
- ✍️ **Autores**: Informações dos autores
- 🏷️ **Categorias**: Classificação dos livros
- 📋 **Empréstimos**: Controle de livros emprestados
- 🔄 **Reservas**: Sistema de reserva de livros

### App Curso

Gerenciamento dos cursos da instituição:

- Cadastro e atualização de cursos
- Associação com alunos e professores
- CRUD completo

### Estrutura de Arquivos Padrão dos Apps

Cada app segue a estrutura Django padrão:

| Arquivo | Responsabilidade |
|---------|------------------|
| `models.py` | Definição das tabelas do banco de dados (ORM Django) |
| `views.py` | Lógica de negócio e processamento de requisições |
| `urls.py` | Roteamento de URLs específicas do app |
| `forms.py` | Formulários para entrada de dados |
| `admin.py` | Configuração da interface administrativa do Django |
| `tests.py` | Testes automatizados |
| `apps.py` | Configuração do app |



## 📦 Dependências

| Pacote | Versão | Propósito |
|--------|--------|----------|
| Django | 5.0 | Framework web principal |
| django-crispy-forms | 2.5 | Renderização avançada de formulários |
| crispy-bootstrap4 | 2025.6 | Tema Bootstrap 4 para formulários |
| psycopg2-binary | 2.9.11 | Driver PostgreSQL |
| dj-database-url | 3.0.1 | Configuração de BD via URL |
| Faker | 35.2.0 | Geração de dados fictícios |
| asgiref | 3.10.0 | Utilitários ASGI |
| sqlparse | 0.5.3 | Parser SQL |

## 🚀 Instalação e Execução

### Pré-requisitos
- Python 3.8+
- pip
- Git

### 1. Clonar o Repositório

```bash
git clone https://github.com/leonhardc/biblioteca.git
cd biblioteca
```

### 2. Criar e Ativar Ambiente Virtual

**Criar o ambiente virtual:**
```bash
python -m venv venv
```

**Ativar no Ubuntu/Linux/macOS:**
```bash
source venv/bin/activate
```

**Ativar no Windows:**
```cmd
venv\Scripts\activate
```

Após ativação bem-sucedida, seu terminal exibirá:
```
(venv) seu_usuario@seu_computador:~/biblioteca$
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar Banco de Dados

Executar migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

Popular com dados de exemplo:
```bash
python povoar_banco.py
// ou
python manage.py shell
>>> from povoar_banco import script_povoar_banco
>>> script_povoar_banco()
```

### 5. Executar a Aplicação

```bash
python manage.py runserver
```

Você verá uma saída similar a:
```
System check identified no issues (0 silenced).
February 13, 2026 - 10:30:45
Django version 5.0, using settings 'biblioteca.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**Acesse:** http://127.0.0.1:8000/

### 6. Acessar o Painel Administrativo

http://127.0.0.1:8000/administrador/

## 📖 Como Usar

### Tipos de Acesso

1. **Aluno**
   - Dashboard com informações pessoais
   - Catálogo de livros
   - Reservar e alugar livros
   - Visualizar histórico de empréstimos

2. **Professor**
   - Mesmas funcionalidades do aluno
   - Limite maior de livros simultâneos
   - Prazo estendido para devoluções

3. **Funcionário**
   - Gerenciar empréstimos (próprios e alheios)
   - Atualizar informações de livros
   - Gerar relatórios
   - Gerenciar devoluções

4. **Administrador**
   - Acesso total ao sistema
   - CRUD completo de todas as entidades
   - Gerenciamento de usuários
   - Configurações do sistema

## 🏛️ Ambiente Virtual - Por Quê?

Isolamento de dependências é crucial ao desenvolver em Python. Um ambiente virtual garante que:

- ✅ Cada projeto tenha suas próprias dependências
- ✅ Conflitos de versões sejam evitados
- ✅ O ambiente global permaneça limpo
- ✅ A aplicação seja facilmente portável

**Exemplo:** Se você instala Django 5.0 globalmente e depois precisa de Django 4.0 em outro projeto, causará conflitos. Com ambientes virtuais, cada projeto é independente.

## 📂 Estrutura de Pastas Resumida

```
biblioteca/
├── biblioteca/              # Configurações principais
├── administrador/           # Painel administrativo
├── usuario/                 # Gerenciamento de usuários
├── livro/                   # Sistema de livros
├── curso/                   # Gerenciamento de cursos
├── notificacao/             # Sistema de notificações
├── static/                  # CSS, JavaScript, imagens
├── templates/               # Templates HTML
├── utils/                   # Funções utilitárias
├── manage.py                # Utilitário Django
├── requirements.txt         # Dependências do projeto
└── db.sqlite3               # Banco de dados SQLite
```

## 🔧 Recursos Principais

### ✨ Implementado
- ✅ CRUD completo de livros, autores e categorias
- ✅ Sistema de empréstimos e reservas
- ✅ Três tipos de usuários com permissões distintas
- ✅ Painel administrativo personalizado
- ✅ Autenticação via Django Auth
- ✅ Banco de dados com ORM Django
- ✅ Sinais Django para automação de tarefas
- ✅ Formulários com validação

### 🚧 Melhorias Futuras
- [ ] Interface mobile responsiva
- [ ] Sistema de notificações por email
- [ ] Relatórios PDF
- [ ] API REST
- [ ] Dashboard com gráficos de uso
- [ ] Importação de livros em lote
- [ ] Sistema de recomendação

## 📝 Notas Importantes

### Arquitetura
Este projeto utiliza:
- **ORM Django** para abstração de banco de dados
- **Django Models** para definição de schemas
- **Django Views** (baseadas em classes e funções)
- **Django Templates** para renderização frontend
- **Django Signals** para lógica automática

### Banco de Dados
- **Desenvolvimento:** SQLite (padrão)
- **Produção:** PostgreSQL (configurável em settings.py)
- Suporte a MySQL/MariaDB via configuração

### Autenticação
Utiliza o sistema de autenticação padrão do Django (`django.contrib.auth.models.User`), economizando desenvolvimento e garantindo segurança.

## 🤝 Contribuindo

Consulte [CONTRIBUTING.md](CONTRIBUTING.md) para informações sobre como contribuir.

Para verificar se suas contribuições estão aparecendo no GitHub, execute:
```bash
./check-contributions.sh
```

## 📄 Documentação Adicional

- [Checklist de Responsividade](CHECKLIST_RESPONSIVIDADE.md)
- [Guia de Paginação Otimizada](PAGINACAO_OTIMIZADA.md)
- [README de Responsividade](README_RESPONSIVIDADE.md)
- [Exemplos de Responsividade](EXEMPLOS_RESPONSIVIDADE.md)

## 🐛 Troubleshooting

### Erro: "No module named 'django'"
**Solução:** Verifique se o ambiente virtual está ativado e se as dependências foram instaladas:
```bash
pip install -r requirements.txt
```

### Erro ao executar migrations
**Solução:** Certifique-se de que está no diretório raiz do projeto e execute:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Porta 8000 já em uso
**Solução:** Execute em porta diferente:
```bash
python manage.py runserver 8001
```

### Banco de dados corrompido
**Solução:** Delete `db.sqlite3` e refaça as migrations:
```bash
rm db.sqlite3
python manage.py migrate
python povoar_banco.py
```

## 📊 Informações do Projeto

| Item | Descrição |
|------|-----------|
| **Linguagem** | Python |
| **Framework** | Django 5.0 |
| **Banco de Dados** | SQLite / PostgreSQL |
| **Padrão de Arquitetura** | MTV (Model-Template-View) |
| **Status** | Em Desenvolvimento |
| **Licença** | - |

## 🎓 Aprendizados

Este projeto foi desenvolvido para consolidar conhecimentos em:
- Modelagem de banco de dados relacional
- Django Framework (Models, Views, Templates)
- HTML/CSS/JavaScript
- Segurança em aplicações web
- Boas práticas de desenvolvimento
- Versionamento com Git

## 📞 Suporte

Para dúvidas ou sugestões:
1. Abra uma [Issue](https://github.com/leonhardc/biblioteca/issues)
2. Consulte a [documentação do Django](https://docs.djangoproject.com/)
3. Verifique os comentários no código

---

**Desenvolvido com ❤️ como projeto educacional**
