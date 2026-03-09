from django import forms
from .models import Turnos

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turnos
        fields = ['nombre', 'desc', 'fecha', 'hora', 'sena']

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-input'
            }),

            'desc': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4
            }),

            'fecha': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-input'
            }),

            'hora': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-input'
            }),

            'sena': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01'
            }),
        }

        labels = {
            'nombre': 'Nombre del cliente',
            'desc': 'Servicio / nota',
            'fecha': 'Fecha',
            'hora': 'Hora',
            'sena': 'Seña ($)',
        }