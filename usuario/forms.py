from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

class SignUpForm(ModelForm):
    username = forms.CharField(required=True,min_length=5,max_length=15)
    first_name = forms.CharField(required=True,min_length=3,max_length=25, label="Nombre(s)")
    last_name = forms.CharField(required=True,max_length=45,label="Apellidos")
    email = forms.EmailField(required=True,max_length=60,label="E-mail")
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        widgets = {
            'password':forms.PasswordInput(),
        }
class EditForm(ModelForm):
    first_name = forms.CharField(required=True,min_length=3,max_length=25, label="Nombre(s)")
    last_name = forms.CharField(required=True,max_length=45,label="Apellidos")
    email = forms.EmailField(required=True,max_length=60,label="E-mail")
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']