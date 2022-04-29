"""
Definition of forms.
"""

from django import forms
from app.models import Pelicula
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class RegistroForm(forms.Form): #Formulario de registro de usuarios
    username = forms.EmailField(required=True) #email
    pass1 = forms.CharField(widget=forms.PasswordInput) #Pass
    pass2 = forms.CharField(widget=forms.PasswordInput) #Pass repetido

class PeliculaForm(forms.ModelForm):
        class Meta:
            model = Pelicula
            fields = ('titulo','direccion','anio','genero','sinopsis','votos')