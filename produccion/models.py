from django.db import models
from users.models import User

class Planta(models.Model):
    codigo = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    codigo = models.CharField(max_length=3, unique=True)
    nombre = models.CharField(max_length=100)
    planta = models.ForeignKey(Planta, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class RegistroProduccion(models.Model):
    TURNOS = (
        ('AM', 'Mañana'),
        ('PM', 'Tarde'),
        ('MM', 'Noche'),
    )

    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    litros = models.PositiveIntegerField()
    fecha = models.DateField()
    turno = models.CharField(max_length=2, choices=TURNOS)
    hora_registro = models.TimeField(auto_now_add=True)
    operador = models.ForeignKey(User, on_delete=models.CASCADE)
    modificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='modificado_por')
    modificado_en = models.DateTimeField(null=True, blank=True)
    eliminado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.producto} - {self.litros} L - {self.turno}'

