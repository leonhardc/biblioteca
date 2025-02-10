# Biblioteca Universitária

Este projeto é desenvolvido diretamente por mim e não tem fins comerciais, contudo tenho como objetivo principal 
mostrar uma série de habilidades que tenho como desenvolvedor web, profissão essa que ainda não pratico mas que
viso com muita determinação e orgulho.

Inicialmente este projeto está sendo desenvolvido em python como linguagem de programação principal e django
como framework.

## Models
### App de Usuário


Este é o primeiro app que se tem acesso nesta aplicação. É importante reforçar que neste projeto não tentei reinventar
a roda, de maneira que, na medida dos meus conhecimentos, tentei aproveitar as funcionalidades que o django já me oferece
para a construção de uma aplicação. Um exemplo disso é que o controle de acesso de usuário inicial é feito usando o model
`User` do módulo `django.contrib.auth.models` do django, que já implementa um caracteristicas como username, first_name, 
last_name, email, password e um pequeno controle de grupo, que será mostrado com mais detalhes mais adiante.


A aplicação de biblioteca consta com 3 models principais que implementam 3 tipos de usuários: O model ALUNO, O models PROFESSOR
e o model FUNCIONÁRIO. 

#### ALUNOS
Levando em consideração a estrutura e as funções de uma biblioteca o app ALUNO foi construido com os seguintes atributos:


```
class Aluno(models.Model):
    usuario = models.ForeignKey(User,...)
    matricula = models.CharField(unique=True, ...)
    curso = models.ForeignKey(Curso, ...)
    endereco = models.CharField(max_length=255, ...)
    cpf = models.CharField(unique=True,max_length=11, ...)
    ingresso = models.DateField(default=datetime.date.today, ...)
    conclusao_prevista = models.DateField(default=datetime.date.today,...)
    ...
```


Relações com outros models como o model User e o model Curso foram implementadas pensando em facilitar pesquisas e diminuir repetição de
código.


#### PROFESSORES
Fazendo as mesmas considerações do model Aluno, foi implementado o model de PROFESSOR assim como o que segue:


```
    class Professor(models.Model):
      JORNADA = (
          ('20', '20hr'),
          ('40', '40hr'),
          ('DE', 'Dedicação Exclusiva'),
      )
      usuario = models.ForeignKey(User,...)
      matricula = models.CharField(unique=True,...)
      curso = models.ForeignKey(Curso,...)
      cpf = models.CharField(unique=True,...)
      regime = models.CharField(max_length=3,...)
      contratacao = models.DateField(default=datetime.date.today,...)

```

#### FUNCIONÁRIOS

```
  class Funcionario(models.Model):
      usuario = models.ForeignKey(User, ...)
      matricula = models.CharField(unique=True, ...)
```
