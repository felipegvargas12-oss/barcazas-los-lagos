from django.core.exceptions import ValidationError
from django.db import models


class Terminal(models.Model):
	nombre = models.CharField(max_length=150, verbose_name='Nombre del terminal o rampa')
	comuna = models.CharField(max_length=100, verbose_name='Comuna')
	estado = models.CharField(max_length=120, verbose_name='Estado operativo')
	marea = models.CharField(max_length=120, verbose_name='Estado de marea')
	es_demostracion = models.BooleanField(default=False, verbose_name='Datos de demostración')

	class Meta:
		ordering = ['nombre', 'comuna']
		verbose_name = 'Terminal o rampa'
		verbose_name_plural = 'Terminales y rampas'

	def __str__(self):
		return f'{self.nombre} ({self.comuna})'

	def clean(self):
		errores = {}
		for campo in ('nombre', 'comuna', 'estado', 'marea'):
			valor = getattr(self, campo, '') or ''
			if valor and not any(caracter.isalnum() for caracter in valor):
				errores[campo] = 'Ingresa al menos una letra o un número; no uses solo signos.'

		if errores:
			raise ValidationError(errores)
