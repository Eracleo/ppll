from django import forms
from pyllik.models import Reserva, Persona
from django.forms.formsets import formset_factory

class PostForm(forms.Form):
    Paquete_Id = forms.CharField(max_length=256)
    Cantidad_Personas = forms.CharField(max_length=256)
    Fecha = forms.DateTimeField()
class ReservarForm(forms.ModelForm):
    class Meta:
        model = Reserva
class ContactoForm(forms.Form):
	correo = forms.EmailField()
	mensaje = forms.CharField(widget=forms.Textarea)
	
class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona

PersonaFormset= formset_factory(PersonaForm, extra=2, max_num=3)

class ReservaaForm(forms.Form):
    paquete= forms.CharField(max_length=100)    
    viajeros= PersonaFormset()
