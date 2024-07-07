from django import forms
from .models import RegistroProduccion

class RegistroProduccionForm(forms.ModelForm):
    class Meta:
        model = RegistroProduccion
        fields = ['producto', 'litros', 'fecha', 'turno']
