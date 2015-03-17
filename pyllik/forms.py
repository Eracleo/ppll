from django import forms
from .models import Paquete, Empresa
class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
        exclude = ('empresa',)
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        exclude = ('user',)
