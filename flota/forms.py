from django import forms

from .models import Embarcacion


class EmbarcacionForm(forms.ModelForm):
    class Meta:
        model = Embarcacion
        fields = [
            'nombre',
            'matricula',
            'capacidad_pasajeros',
            'capacidad_vehicular',
            'activo',
        ]
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: Barcaza Lago Sur',
                }
            ),
            'matricula': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ej: BLS-2026',
                }
            ),
            'capacidad_pasajeros': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la capacidad de pasajeros',
                    'min': 1,
                }
            ),
            'capacidad_vehicular': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la capacidad vehicular',
                    'min': 0,
                }
            ),
            'activo': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                }
            ),
        }

    def clean_matricula(self):
        matricula = self.cleaned_data.get('matricula')
        if matricula is None:
            return matricula

        matricula = matricula.strip().upper()
        if len(matricula) < 4:
            raise forms.ValidationError('La matrícula debe tener al menos 4 caracteres.')

        return matricula

    def clean_capacidad_pasajeros(self):
        capacidad = self.cleaned_data.get('capacidad_pasajeros')

        if capacidad is None:
            return capacidad

        if capacidad <= 0:
            raise forms.ValidationError('La capacidad de pasajeros debe ser mayor a 0.')

        return capacidad
