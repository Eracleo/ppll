# -*- coding: utf-8 -*-
from django import forms
from .models import Paquete, Empresa
from suit_ckeditor.widgets import CKEditorWidget

class PaqueteForm(forms.ModelForm):
    precio = forms.FloatField(required=True,min_value=0,help_text="Coloque el precio del paquete, tal como aparece en su sitio web. Los precios son en Dólares Americanos (USD $)")
    class Meta:
        model = Paquete
        fields = ('sku','nombre', 'precio','porcentaje','pre_pago','descripcion','link','estado')
        widgets = {
            'sku': forms.HiddenInput(),
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
        exclude = ('user','nro_paquetes','paypal_email','paypal_at')

class EmpresaFormEdit(forms.ModelForm):
    razon_social = forms.CharField(max_length=40)
    direccion = forms.CharField(max_length=40)
    telefono = forms.CharField(max_length=30)
    ruc = forms.CharField(min_length=11)
    class Meta:
        model = Empresa
        exclude = ('user','nro_paquetes','paypal_email','paypal_at','abreviatura')

class PaypalAccountForm(forms.ModelForm):
    paypal_email = forms.CharField(required=True,max_length=60)
    paypal_at = forms.CharField(required=True,max_length=64)
    class Meta:
        model = Empresa
        exclude = ('user','nro_paquetes','direccion','razon_social','telefono','rubro','ruc','web','logo','terminos_condiciones','abreviatura')