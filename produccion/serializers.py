from rest_framework import serializers
from .models import RegistroProduccion

class RegistroProduccionSerializer(serializers.ModelSerializer):
    producto = serializers.SerializerMethodField()
    operador = serializers.SerializerMethodField()
    modificado_por = serializers.SerializerMethodField()

    class Meta:
        model = RegistroProduccion
        fields = '__all__'

    def get_producto(self, obj):
        return obj.producto.nombre

    def get_operador(self, obj):
        return obj.operador.username  # Asumiendo que User tiene un campo 'username'

    def get_modificado_por(self, obj):
        return obj.modificado_por.username if obj.modificado_por else None  # Manejar casos donde modificado_por es null


class ProduccionPorPlantaSerializer(serializers.Serializer):
    planta = serializers.CharField(source='producto__planta__nombre')
    producto = serializers.CharField(source='producto__nombre')
    total_litros = serializers.IntegerField()