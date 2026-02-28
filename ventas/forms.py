from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        # Aquí listamos los campos que quieres que aparezcan en el formulario para rellenar
        fields = ['nombre', 'precio', 'descripcion', 'stock', 'imagen']
        
        # Esto es para que se vea lindo (opcional, pero ayuda al orden)
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción breve'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'precio': 'Precio ($)',
            'stock': 'Cantidad Disponible',
            'imagen': 'Foto del Producto'
        }