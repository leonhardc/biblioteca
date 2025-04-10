from django import forms
from usuario.models import Aluno
from curso.models import Curso
from django.core.exceptions import ValidationError
import re