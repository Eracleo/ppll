from django import forms
from .models import Paquete

class PostForm(forms.Form):
    Paquete_Id = forms.CharField(max_length=256)
    Cantidad_Personas = forms.CharField(max_length=256)
    Fecha = forms.DateTimeField()

#Clase para editar paquetes
class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
