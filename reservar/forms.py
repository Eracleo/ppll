from django import forms
from pyllik.models import Pasajero
from django.forms.formsets import formset_factory

class PasajeroForm(forms.ModelForm):
    nombre = forms.CharField(required=True,max_length=15)
    class Meta:
        model = Pasajero
        exclude = ('editado','creado')