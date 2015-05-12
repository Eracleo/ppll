# -*- coding: utf-8 -*-
from django import forms
from .models import Paquete, Empresa, Pasajero, Cliente,Reserva,Trabajador
from django.contrib.auth.models import User
from suit_ckeditor.widgets import CKEditorWidget

class PaqueteForm(forms.ModelForm):
    precio = forms.FloatField(required=True,min_value=0,help_text="Coloque el precio del paquete, tal como aparece en su sitio web. Los precios son en Dólares Americanos (USD $)")
    class Meta:
        model = Paquete
        fields = ('nombre', 'precio','porcentaje','pre_pago','descripcion','link','estado')
        widgets = {
            'descripcion': CKEditorWidget(editor_options={'startupFocus': True})
        }
class PaqueteEditForm(forms.ModelForm):
    precio = forms.FloatField(required=True,min_value=0,help_text="Coloque el precio del paquete, tal como aparece en su sitio web. Los precios son en Dólares Americanos (USD $)")
    class Meta:
        model = Paquete
        fields = ('nombre', 'precio','porcentaje','pre_pago','descripcion','link','estado')
        widgets = {
            'descripcion': CKEditorWidget(editor_options={'startupFocus': True})
        }
class EmpresaForm(forms.ModelForm):
    razon_social = forms.CharField(min_length=3,max_length=40)
    direccion = forms.CharField(max_length=40)
    telefono = forms.CharField(max_length=30)
    ruc = forms.CharField(min_length=11)
    abreviatura = forms.CharField(min_length=3)
    class Meta:
        model = Empresa
        fields  = ('rubro','ruc','razon_social','direccion','abreviatura','telefono',)
class EmpresaFormEdit(forms.ModelForm):
    razon_social = forms.CharField(max_length=40)
    direccion = forms.CharField(max_length=40)
    telefono = forms.CharField(max_length=30)
    ruc = forms.CharField(min_length=11)
    class Meta:
        model = Empresa
        exclude = ('trabajadores','logo','nro_paquetes','paypal_email','paypal_at','abreviatura')
class EmpresaFormEditLogo(forms.ModelForm):
    class Meta:
        model = Empresa
        fields  = ('logo',)
class PaypalAccountForm(forms.ModelForm):
    paypal_email = forms.CharField(required=True,max_length=60)
    paypal_at = forms.CharField(required=True,max_length=64)
    class Meta:
        model = Empresa
        fields  = ('paypal_email','paypal_at',)
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('nombre','apellidos', 'doc_tipo','doc_nro','email','telefono','celular','pais')
class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ('doc_nro','direccion','doc_nro','telefono','celular')
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password',)
        widgets = {
            'password':forms.PasswordInput(),
        }
class PasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        exclude = ('editado','creado')
class ReservaEstadoForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields  = ('estado','estado_pago',)
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields=('fecha_viaje','cantidad_pasajeros','estado_pago','reservado_mediante','estado',)
# Buscar
class BuscarReservaForm(forms.ModelForm):
    def __init__(self, empresa_id=1, *args, **kwargs):
        super(BuscarReservaForm, self).__init__(*args, **kwargs)
        self.fields['paquete'].queryset = Paquete.objects.filter(empresa_id=empresa_id)
    class Meta:
        model = Reserva
        fields = ('fecha_viaje','estado','estado_pago','paquete',)
class BuscarClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ('email','pais',)
class BuscarPasajeroForm(forms.ModelForm):
    class Meta:
        model = Pasajero
        fields = ('doc_nro','pais',)