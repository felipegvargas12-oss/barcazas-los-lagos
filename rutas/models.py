from django.db import models
from django.core.exceptions import ValidationError

def validar_precio_positivo(value):
    if value <= 0:
        raise ValidationError('El precio base debe ser mayor a $0.')

class Ruta(models.Model):
    origen = models.CharField(max_length=100, verbose_name="Puerto de Origen")
    destino = models.CharField(max_length=100, verbose_name="Puerto de Destino")
    duracion_horas = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="Duración (Horas)")
    precio_base = models.IntegerField(validators=[validar_precio_positivo], verbose_name="Precio Base ($)")
    activa = models.BooleanField(default=True, verbose_name="¿Ruta Activa?")
    es_demostracion = models.BooleanField(default=False, verbose_name="Datos de demostración")
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Regla personalizada: Origen y Destino no pueden ser iguales
        if self.origen and self.destino and self.origen.strip().lower() == self.destino.strip().lower():
            raise ValidationError({'destino': 'El puerto de destino no puede ser igual al puerto de origen.'})

    def __str__(self):
        return f"{self.origen} ➔ {self.destino}"


class Horario(models.Model):
    ruta = models.ForeignKey(
        Ruta,
        on_delete=models.CASCADE,
        related_name='horarios',
        verbose_name='Ruta',
    )
    salida = models.DateTimeField(verbose_name='Fecha y hora de salida')
    activo = models.BooleanField(default=True, verbose_name='Salida disponible')

    class Meta:
        ordering = ['salida']
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'

    def __str__(self):
        return f"{self.ruta} - {self.salida:%d/%m/%Y %H:%M}"