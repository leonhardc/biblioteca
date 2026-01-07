# Biblioteca Universitária

> **📌 Nota sobre Contribuições:** Se suas contribuições para este projeto não estão aparecendo no seu perfil do GitHub, consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para soluções e configurações necessárias.

## Sobre o projeto

<p align='justify' style='text-indent: 40px;'>
Biblioteca universitária foi o projeto final na disciplina de banco de dados quando cursei Engenharia de Computação e segue uma descrição de requisitos específica da disciplina. Porém, por mais que este projeto tenha muito daquele que foi desenvolvido na época, o que vos aprosento é um projeto pessoal, pensado e estruturado inteiramente por mim levando em consideração o que aprendi na época e também o que aprendi posteriormente.</p>

<p align='justify' style='text-indent: 40px;'>
A primeira vez que desenvolvi essa aaplicação ainda estava aprendendo sobre banco de dados e o foco principal era o banco de dados. Na época não pude utilizar estruturas que usei para desenvolver este projeto (como o ORM do django, por exemplo). Infelizmente, não salvei o projeto que desenvolvi na disciplina por não ter noções de versionamento de código com o git.</p>

<p align='justify' style='text-indent: 40px;'>
Neste projeto fiz desde a modelagem do banco de dados até o design das janelas. Desde a configuração dos apps, até a implementação das views de cada app django. Aqui usei tudo o que sei até o momento sobre desenvolvimento, sobre aplicações web, sobre django e sobre banco de dados.</p>

<p align='justify' style='text-indent: 40px;'>
Mas enfim, o que é o projeto? Do que se trata toda essa codificação? Biblioteca universitária, ou biblioteca acadêmica, é uma aplicação web, desenvolvida em django (framework python para web) e que tem como idéia principal o gerenciamento do acervo de livros por uma instituição de ensino fictícia e que conta com três tipos de usuários principais (fora os administradores), que são os alunos, os professores e os funcionários. Todos esses usuários serão descritos com mais detalhes posteriormente. Cada um desses usuários pode reservar ou alugar um ou mais livros, por um determinado tempo.</p>

<p align='justify' style='text-indent: 40px;'>
Todas as entidades serão descrita com detalhes nas seções seguintes onde primeiro será descrito o app em sí e o que ele representa na aplicação. Depois de abordarmos o sentido geral de um app navegaremos por cada arquivo e o que ele representa dentro de cada contexto. Por fim, o projeto também contará com uma seção contando como rodar a aplicação localmente com demonstrações de comandos e um vídeo mostrando como a aplicação roda na minha máquina e como deveria rodar na máquina de quem está lendo.</p>

## Estrutura do Projeto

<p align='justify' style='text-indent: 40px;'>
O projeto conta com 4 apps até o momento, cada um tem um sentido por existir e claro, contém também o app principal onde estão as configurações gerais do projeto. A estrutura de pastas do projeto é a seguinte:</p>

```
- biblioteca/
    |-biblioteca/
    |-administrador/
    |-usuario/
    |-livro/
    |-curso/
    |-static/
    |-templates/
    |-utils/
```

### O primeiro app, o app biblioteca

<p align='justify' style='text-indent: 40px;'>
O primeiro app é o app principal da aplicação onde estão principalmente as  configurações do projeto. Sua estrutura é a seguinte:</p>

```
|-biblioteca/
    asgi.py
    settings.py
    urls.py
    wsgi.py
```

<p align='justify' style='text-indent: 40px;'>
Como dito anteriormente, nesse app são guardadas as configurações gerais e primeiras da aplicação como um todo. Por exemplo, no arquivo "settings.py" estão configurações de bancos de dados (sqlite, mysql, mogodb, mariadb etc.), configurações de como a aplicação enxerga os apps, configurações de qual será o diretório principal de templates e até configurações do framework de mensagens do django.</p>

<p align='justify' style='text-indent: 40px;'>
No arquivo "urls.py" estão as urls dos apps da aplicação. Neste projeto está configurado da seguinte maneira:</p>

```python
urlpatterns = [
    path('admin/', admin.site.urls), # admin padrão do django
    path('administrador/', include('administrador.urls')), # admin personalizado
    path('usuario/', include('usuario.urls')),
    path('livro/', include('livro.urls')),
    path('curso/', include('curso.urls')),
]
```

<p align='justify' style='text-indent: 40px;'>
Todas as urls mostradas acima serão explicadas com mais detalhes posteriormente quando de fato estivermos navegado em seu respectivo app. O bloco acima só foi um exemplo sobre o que existe dentro desse arquivo.</p>

<!-- TODO: Pesquisar sobre as funções dos arquivos asgi.py e wsgi.py no app principal de uma aplicação django. -->
<p align='justify' style='text-indent: 40px;'>
Os arquivos "asgi.py" e "wsgi.py" não serão abordados nesta explicação por enquanto.</p>

### O app administrador

<p align='justify' style='text-indent: 40px;'>
O app administrador é uma maneira de me forçar a pensar e implementar todas as funções da aplicação, aquelas que estão acessíveis para outros usuários e aquelas que não. Em tese, depois que este app estiver pronto, a implementação dos apps seguintes se tornará mais fácil.</p>

<p align='justify' style='text-indent: 40px;'>
Vale lembrar que o próprio django já implementa uma página de administrador por padrão e eu sei que reinventar a roda não é uma idéia muito prática, porém, estou aprendendo e todo esforço é bem vindo desde que isso se converta em aprendizado posteriormente. Por isso, implementei um app que, teoricamente contém todas as funcionalidades de administrador do sistema. Com CRUD completo e com operações personalidas sobre todas as entidades do sistema tanto usuários quanto livros ou cursos.</p>

<p align='justify' style='text-indent: 40px;'>
A estrutura desse app é como a estrutura dos apps seguintes e conta com os mesmos arquivos. Sendo assim a estrutura desse app é como mostrada abaixo:</p>

```
|-administrador/
    admin.py
    apps.py
    forms.py
    models.py
    tests.py
    urls.py
    views.py
```

<p align='justify' style='text-indent: 40px;'>
É importante esclarecer que esses arquivos contém implementações de algumas das muitas funcionalidades da aplicação e não vale muito a pena mostrar, a você leitor, tudo que contém dentro de cada um, porque isso irá se tornar cansativo, tanto pra mim quanto pra você. Então vamos para algumas explicações básicas sobre cada um:</p>

1. <p align='justify'><strong>admin.py</strong>: Aqui você configura como app vai se comportar na página de administração padrão do django e como os models serão mostrados e que informações serão mostradas em cada model.</p>
2. <p align='justify'><strong>apps.py</strong>: Particularmente até hoje não tive que mecher nesse arquivo e até hoje não sei bem pra que ele funciona, porém é para ele que você aponta (lá em biblioteca/settings.py por exemplo) quando inicia um novo app na aplicação e quer que ele seja reconhecido pelo django.</p>
3. <p align='justify'><strong>forms.py</strong>: Sinceramente esse arquivo aqui não vem por padrão quando você inicia um novo app no django, porém é recomendado criar esse arquivo quando seu app vai gerenciar formulários, como formulários de informações usuários ou formulários de cadastro de livros, por exemplo.</p>
4. <p align='justify'><strong>models.py</strong>: É aqui onde são declarados todos os seus models. Ou seja, classes que serão interpretadas e transformadas em tabelas no seu banco de dados. Aconselho ter bastante cuidado, porque editar os models.py dá trabalho e se não for bem pensado e estruturado desde o começo pode dar uma dor de cabeça lá na frente.</p>
5. <p align='justify'><strong>tests.py</strong>: O django também conta com um mecanismo pra você implementar testes e executá-los de maneira simples e semântica e é nesse arquivo onde você irá implementá-los.</p>
6. <p align='justify'><strong>urls.py</strong>: Nesse arquivo aqui irão ficar todas as suas urls, ou pelo menos todas as urls do seu app se você pensar bem. Falo mais sobre isso depois, mas no fim, são sempre os meios de você chamar as funcionalidades da sua aplicação.</p>
7. <p align='justify'><strong>views.py</strong>: É aqui onde o filho chora e a mãe não vê. É aqui onde a mágica acontece. É aqui onde todas as vontades de desistir irão vir a tona (ou pelo menos boa partes delas). Como o nome deixa bem claro, é aqui onde suas views estão, em resumo, onde todas as funções ou regras de negócios vão atuar. É aqui onde você mostra o que seu app faz, como faz, porque faz e quando faz. É aqui onde você vai implementar seu CRUD, onde vai direcionar tudo para os mais variados endpoints e onde você vai chorar, e chorar muito.</p>

<p align='justify' style='text-indent: 40px;'>
Bem, até agora eu não expliquei muito sobre minha solução em si, mas prometo, vamos chegar lá. Nas próximas três subseções irei mostrar o que forma basicamente o nucleo do projeto, os apps de usuários, livros e cursos.</p>

### O app usuario

<p align='justify' style='text-indent: 40px'>
Falamos anteriormente do app que representa o nosso usuário administrador, aquele que pode, teoricamente, fazer qualquer coisa no nosso sistema. Agora, vamos falar do app que representa os outros usuários da aplicação. Aqueles que de fato são usuários, os que não vão fazer nada além do permitido a eles fazer.</p>

<p align='justify' style='text-indent: 40px'>
Falar assim é um pouco estranho eu sei, mas é basicamente isso. Cada um dos seguintes usuários vai contar com um numero limitado de informações e funcionalidades as quais vai conseguir cisualizar e acessar. Estes usuários são descritos logo abaixo:</p>

-   <p align='justify'>O usuário <strong>aluno</strong>: Esse é o tipo de usuário mais populoso na nossa aplicação mas que terá menos poder nas mãos. O usuário aluno é uma abstração dos alunos da nossa instituição de ensino ficticia. Ele pode basicamente visualizar suas proprias informações, ver uma lista de livros os quais ele pode ver suas informações básicas, pode reservar um exemplar que será posteriormente alugado e claro, ele tem acesso à todas as reservas e emprestimos que ele tem ativos. De todos os usuários, ele é quem pode alugar menos livros.</p>
-   <p align='justify'>O usuário <strong>professor</strong>: O usuário professor pode fazer basicamente as mesmas coisas que um aluno porém ele pode alugar uma quantidade maior de livros e por um tempo maior.</p>
-   <p align='justify'>O usuário <strong>funcionário</strong>: Este tipo de usuário pode fazer tudo que os outros usuários pode fazer. Sim, ele também pode alugar livros para si. Em adicional, o funcionário também pode alugar livros para outros funcionários e outros usuários, tanto professores quanto alunos. O funcionário pode ver e alterar informações de livros, atualizando-os no banco de dados. Lembrando que o funcionário não deve ser capaz de alterar informações de outros usuários, tanto professores quanto alunos.</p>

<p align='justify' style='text-indent: 40px'>
Agora que você leitor já sabe um pouco sobre cada tipo de usuário que a nossa aplicação tem, você pode talvez estar curioso sobre como cada um deles está implementado na base de dados. Hoje, no dia que estou escrevendo esta descrição, a implementação não está totalmente completa. Existem algumas coisas que podem ser implementadas para deixar os models desses usuários mais completa. Mas aqui vai uma palhinha de como as coisas estão ficando.</p>

```python
# Model do usuário 'aluno'
class Aluno(models.Model):
    usuario = models.ForeignKey(User, ...)
    matricula = models.CharField(...)
    curso = models.ForeignKey(Curso, ...)
    endereco = models.CharField(...)
    cpf = models.CharField(...)
    ingresso = models.DateField(...)
    conclusao_prevista = models.DateField(...)

    def __str__(self):
        return f'<{self.usuario}>'

    class Meta:
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'

# Model do usuário 'professor'
class Professor(models.Model):
    usuario = models.ForeignKey(User, ...)
    matricula = models.CharField(...)
    curso = models.ForeignKey(Curso, ...)
    cpf = models.CharField(...)
    regime = models.CharField(...)
    contratacao = models.DateField(...)

    def __str__(self):
        return f'{self.usuario.first_name} {self.usuario.last_name}'

    class Meta:
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'

# Model do usuário 'funcionario'
class Funcionario(models.Model):
    usuario = models.ForeignKey(User, ...)
    matricula = models.CharField(...)
    cpf = models.CharField(...)

    def __str__(self):
        return f'<{self.usuario}>'

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
```

<p align='justify' style='text-indent: 40px'>
Se você é um desenvolvedor mais experiente, facilmente vai olhar para essas classes e notar que está faltando algumas informações. Quer um exemplo? Todo usuário poderia ter uma variável booleana que indica de aquele aluno está ativo ou não, o que significaria que ele foi desligado da instituição. Eu sei, esse projeto tem falhas e problemas que podem ou não ser corrigidos posteriormente para se parecer com uma aplicação mais robusta mas tenha um pouco de paciência.</p>

    "Ah Leonardo, todos esses models poderiam herdar de um outro model que tem informações comuns a todos. Um model 'usuário' por exemplo."

<p align='justify' style='text-indent: 40px'>
Sim gafanhoto, eu sei. Nem tudo aqui foi tão bem pensado quanto eu queria que fosse, mas foi pensado e tem um porquê de existir. Eu estou estudando boas práticas, mas nem sempre você irá encontrar boas práticas no meu código. Dá pra melhorar muita coisa, eu sei, mas estou aprendendo, então tenha paciência.</p>

<p align='justify' style='text-indent: 40px'>
Note que todos os tipos de usuários mostrados acima tem um primeiro atributo e esse atributo está ligado a um outro model chamado 'User'. Pra você que está começando no django, esse model já vem quando você instala o django no seu ambiente. Você pode importá-lo do pacote <strong>django.contrib.auth.models</strong>. Fiz isso porque quero, nesse projeto, usar o controle de usuário do próprio django. Isso vai me economizar muito trabalho.</p>

### O app livro

<p align='justify' style='text-indent: 40px'>
Não se faz uma biblioteca sem livros, não é mesmo? É nesse app que você encontra nossa abstração de livros, com seus autores e suas categorias, todos com seus models e suas respectivas views, dando mais um pouco de funcionalidade a nossa aplicação.</p>
<p align='justify' style='text-indent: 40px'>
Nesse app você também pode encontrar reservas e emprestimos de livros. Essas operações representam o ato de reservar e o ato de pegar emprestado um livro por um determinado tempo. Não acho que seja muito interessante encher sua tela de código (por mais que você esteja lendo algo no github), então vamos adiantar e mostrar a vocẽ só o importante. Abaixo seguem algumas imagens de como é nossa janelinha que vai controlar as operações com a entidade livro e suas variantes:</p>
<!-- TODO: Inserir algumas imagens de exemplo na janela de livro -->

### O app curso

<p align='justify' style='text-indent: 40px'>
Bem, nesse app você encontra nossa abstração dos cursos de uma instituição de ensino. Se vocẽ pensa o mesmo que eu, esse não vai ser o app mais funcional ou mais interessante do sistema. Talvez não precizasse nem de um app dedicado unicamente a essa funcionalidade. Mas eu quiz fazer assim. Então, nesse ponto não espere encontrar muito mais do que um CRUD (rs). Mesmo assim, segue uma demonstração em imagens do que seria a nossa janela que irá administrar os cursos cadastrados na plataforma</p>
<!-- TODO: Inserir algumas imagens de exemplo na janela de livro -->

## Dependências

## Rodando localmente a aplicação

<p align='justify' style='text-indent: 40px'>
Nesta seção você vai aprender a instalar e rodar essa aplicação localmente. Algumas informações que eu ache importante que você leia posteriormente na documentaçao do django ou de outra dependencia irei deixar no final dessa seção.</p>

### Baixando o aplicativo

<p align='justify' style='text-indent: 40px'>
A maneira mais simples de você baixar essa aplicação é fazendo um git clone. Lembrando que algumas instruções desse tutorial pode mudar de sistema para sistema. Eu desenvolvi essa aplicação usando vscode e como sistema operacional o ubuntu 24.04, fique ciente disso quando for rodar a aplicação em windows ou mac, por exemplo.</p>

<p align='justify' style='text-indent: 40px'>
Abra o terminal e digite:</p>

```
git clone https://github.com/leonhardc/biblioteca.git
```

<p align='justify' style='text-indent: 40px'>
Depois de apertar o enter e esperar a operação acabar, você terá todos os arquivos necessários para rodar a aplicação no seu computador. Agora vamos para o próximo passo.</p>

### Instalando o ambiente virtual (opcional)

<p align='justify' style='text-indent: 40px'>
Leia com atenção, principalmente se você está iniciando na programação e quer usar um exemplo como esse repositório para começar a ver como o django funciona.</p>
<p align='justify' style='text-indent: 40px'>
A instalação de um ambiente virtual é muito importante ao desenvolver os seus próprios projetos ou para rodar ambientes de terceiros. Pense comigo, se hoje você dicide começar a desenvolver um e-comerce em django e instala todos as suas dependencias no ambiente global. Ali você vai usar o django mais recente até o momento. Depois de um tempo você trava, não sabe muito bem como configurar o ambiente e seu projeto está com alguns bugs. Você então decide baixar um projeto de um terceiro para vê-lo rodando e usar uma parte do código dele como exemplo para o seu, afinal de contas você ainda está apredendo.</p>
<p align='justify' style='text-indent: 40px'>
Ai você todo animado, vai lá e instala todas as dependencias do projeto do amiguinho no ambiente global da sua máquina, vê que o amiguinho implementou algumas coisas que ajudam a resolver os problemas que vocẽ estava tendo e dai, quando você vai rodar o projeto do amiguinho corre tudo bem, você vê tudo funcionando perfeitamente e quando você volta finalmente para o seu projeto, nada mais funciona. O que você faz? Será alguma biblioteca que está desatualizada? O django está desatualizado? O que aconteceu?</p>
<p align='justify' style='text-indent: 40px'>
Finalmente vocẽ consegue atualizar todas as bibliotecas e dependencias do seu projeto mas quando volta no projeto do seu amigo já não roda nada. O que você faz?</p>
<p align='justify' style='text-indent: 40px'>
Agora imagina se existisse uma forma de isolar as dependencias do seu projeto das dependencias do projeto da pessoa que desenvolveu o projeto que você está usando como base pro seu. Existe, se chama ambiente virtual.</p>
<p align='justify' style='text-indent: 40px'>
Cada linguagem tem seu jeito de instalar um ambiente virtual, em python você pode fazer assim:</p>

```python
python -m venv <nome_do_ambiente>
```

<p align='justify' style='text-indent: 40px'>
Se correr tudo bem, depois que você executar o comando acima uma nova pasta será criada dentro do diretório do seu projeto. Dai, basta você ativar o seu ambiente.</p>

<p align='justify' style='text-indent: 40px'>
No ubuntu, para executar o seguinte comando:</p>

```
source <nome_do_ambiente>/bin/activate
```

<p align='justify' style='text-indent: 40px'>
Se tudo correu bem, o seu terminal vai ficar mais ou menos assim:</p>

```
(<nome_do_seu_ambiente_virtual>) <seu_usuario>@<diretorio_atual>
```

<p align='justify' style='text-indent: 40px'>
Pode variar um pouco, mas o importante é saber que, se o ambiente está ativado corretamente, o nome dele vai aparecer entre parenteses logo antes da linha de comando no seu terminal.</p>

### Instalando as dependencias do projeto

<p align='justify' style='text-indent: 40px'>
Se tudo correu bem até agora e você conseguiu baixar o projeto, instalar e ativar o ambiente virtual na sua máquina, então podemos ir adiante.</p>
<p align='justify' style='text-indent: 40px'>
Veja que no diretório raiz do projeto existe um arquivo chamado <strong>requirements.txt</strong/>. Se você der dois cliques nesse arquivo, o que verá será uma lista de bibliotecas que são, exatamente, as dependencias desse projeto. Para instalá-las, basta executar o comando abaixo:</p>

```
pip install -r requirements.txt
```

<p align='justify' style='text-indent: 40px'>
Tudo bem até aqui? Se sim vamos aprender agora a rodar a aplicação.</p>

### Executando a aplicação na sua máquina (finalmente)

<p align='justify' style='text-indent: 40px'>
Bem, antes de rodar a aplicação de fato (rs), devemos fazer algumas coisas. Como fazer as migrations para o banco de dados:</p>

```python
python manage.py makemigrations
python manage.py migrate
```

<p align='justify' style='text-indent: 40px'>
Os dois comandos acima irão preparar o banco de dados para receber os dados que serão salvos no passo seguinte.</p>

```python
python povoar_banco.py
```

<p align='justify' style='text-indent: 40px'>
O comando acima vai preencher o banco de dados com alguns dados fictícios o que facilita a ter noção de todas as funcionalidades da nossa aplicação.</p>

<p align='justify' style='text-indent: 40px'>
Depois de seguir com todos os passos acima, para executar tudo basta digitar o comando:</p>

```python
python manage.py runserver
```

<p align='justify' style='text-indent: 40px'>
Se tudo correu bem até agora você pode ver uma mensagem como a seguinte no seu terminal:</p>

```
System check identified no issues (0 silenced).
June 23, 2025 - 16:27:56
Django version 5.0, using settings 'biblioteca.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

<p align='justify' style='text-indent: 40px'>
Acessando o endereço http://127.0.0.1:8000/ no seu navegador, você pode ver a aplicação de fato funcionando.</p>
