from rest_framework import serializers
from .models import Ruta

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'

    # Validación personalizada (Ejemplo: no permitir precios negativos o cero)
    def validate_precio_base(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio base debe ser mayor a 0.")
        return value