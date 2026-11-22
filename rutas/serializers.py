from rest_framework import serializers
from .models import Ruta

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'

    def validate(self, data):
        campos_precio = ['precio_base', 'precio_moto', 'precio_auto', 'precio_camion']
        for campo in campos_precio:
            if campo in data and data[campo] < 0:
                raise serializers.ValidationError({campo: "El precio no puede ser negativo."})
        return data