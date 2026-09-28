from django.db import models


class Embarcacion(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    matricula = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name='Matrícula',
        help_text='Número o código único de identificación de la barcaza.'
    )
    capacidad_pasajeros = models.PositiveIntegerField(verbose_name='Capacidad de pasajeros')
    capacidad_vehicular = models.PositiveIntegerField(verbose_name='Capacidad vehicular')
    activo = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Embarcación'
        verbose_name_plural = 'Embarcaciones'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
