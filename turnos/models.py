from django.db import models
class Turnos(models.Model):
    nombre= models.CharField(max_length=100)
    desc = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    hora = models.TimeField()
    sena = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
            return f"{self.nombre} - {self.fecha} {self.hora}"