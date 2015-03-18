from django import forms
from .models import Paquete, Empresa
class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
        fields = ('sku','nombre', 'precio','porcentaje','pre_pago','descripcion','link','estado')
class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        exclude = ('user','nro_paquetes')
