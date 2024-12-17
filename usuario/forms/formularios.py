from django import forms

class LoginForm(forms.Form):
    usuario = forms.CharField(label='Usuário', max_length=255, 
                            widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Usuário', 'style': 'background-color:#e5ebf4'}))
    senha = forms.CharField(label='Senha', max_length=255, 
                            widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Senha', 'style': 'background-color:#e5ebf4'}))