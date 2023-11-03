from django import forms

class AgregarRolForm(forms.Form):
    nombre = forms.CharField(max_length=20, label='Nombre del Rol')

