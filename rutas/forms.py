from django import forms
from .models import Ruta

class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ['origen', 'destino', 'duracion_horas', 'precio_base', 'activa']
        widgets = {
            'origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Puerto Montt'}),
            'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Chaitén'}),
            'duracion_horas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'precio_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'activa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }