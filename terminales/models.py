from django.db import models

class Terminal(models.Model):
    MAREA_CHOICES = [
        ('alta', 'Marea Alta'),
        ('baja', 'Marea Baja'),
        ('todas', 'Operativo en toda marea'),
    ]

    ESTADO_CHOICES = [
        ('operativo', 'Operativo'),
        ('cerrado', 'Cerrado'),
        ('mantenimiento', 'En mantenimiento'),
    ]
    
    nombre = models.CharField(max_length=120)
    marea = models.CharField(max_length=20, choices=MAREA_CHOICES, default='todas')
    comuna = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='operativo')

    class Meta:
        verbose_name = "Terminal o Rampa"
        verbose_name_plural = "Terminales y Rampas"

    def __str__(self):
        return f"{self.nombre} ({self.comuna})"