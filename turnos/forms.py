from django import forms
from .models import Turnos

class TurnoForm(forms.ModelForm):
    class Meta:
        model = Turnos
        fields = ['nombre', 'desc', 'fecha', 'hora', 'sena']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'nombre': 'Nombre del cliente',
            'desc': 'Servicio / nota',
            'fecha': 'Fecha',
            'hora': 'Hora',
            'sena': 'Seña ($)',
        }
