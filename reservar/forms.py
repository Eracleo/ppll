from django import forms
from pyllik.models import Reserva, Persona
from django.forms.formsets import formset_factory

class PostForm(forms.Form):
    Paquete_Id = forms.CharField(max_length=256)
    Cantidad_Personas = forms.CharField(max_length=256)
    Fecha = forms.DateTimeField()