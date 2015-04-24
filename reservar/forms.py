from django import forms
from pyllik.models import Persona
from django.forms.formsets import formset_factory

class PersonaForm(forms.ModelForm):
    nombre = forms.CharField(required=True,max_length=15)
    class Meta:
        model = Persona
        exclude = ('editado','creado')