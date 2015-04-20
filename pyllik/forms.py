# -*- coding: utf-8 -*-
from django import forms
from .models import Paquete, Empresa
from suit_ckeditor.widgets import CKEditorWidget
class PaqueteForm(forms.ModelForm):
    class Meta:
        model = Paquete
        fields = ('sku','nombre', 'precio','porcentaje','pre_pago','descripcion','link','estado')
        widgets = {
            'sku': forms.HiddenInput(),
            'descripcion': CKEditorWidget(editor_options={'startupFocus': True})
        }
class EmpresaForm(forms.ModelForm):
    razon_social = forms.CharField(max_length=40)
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
    abreviatura = forms.CharField(min_length=3)
    class Meta:
        model = Empresa
        exclude = ('user','nro_paquetes','logo','abreviatura')