from django.db import models

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField()
   

    def __str__(self):
        return self.nombre