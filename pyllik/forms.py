from django import forms
from .models import Paquete, Empresa
class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
