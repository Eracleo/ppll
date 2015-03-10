from django import forms
from pyllik.models import Reserva, Persona

class PostForm(forms.Form):
    Paquete_Id = forms.CharField(max_length=256)
    Cantidad_Personas = forms.CharField(max_length=256)
    Fecha = forms.DateTimeField()
class ReservarForm(forms.ModelForm):
    class Meta:
        model = Reserva
