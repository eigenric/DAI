from django import forms
from .models import Receta
from django.core.exceptions import ValidationError

def validar_mayuscula(texto):
    """Devuelve un error de validación del formulario si algún campo no empieza por mayúscula"""
    
    if not texto[0].isupper():
        raise ValidationError("El texto debe comenzar por mayúscula", params={'texto': texto})


class RecetaForm(forms.ModelForm):
    nombre = forms.CharField(max_length=200, validators=[validar_mayuscula])
    preparación = forms.CharField(widget=forms.Textarea, max_length=5000, validators=[validar_mayuscula])
    foto = forms.FileField(label="Selecciona un archivo")

    class Meta:
        model = Receta
        fields = "__all__"