from rest_framework import serializers
from .models import RegistroProduccion,Producto, User

class RegistroProduccionSerializer(serializers.ModelSerializer):
    producto = serializers.SlugRelatedField(slug_field='nombre', queryset=Producto.objects.all())
    operador = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), required=False)
    modificado_por = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), required=False)

    class Meta:
        model = RegistroProduccion
        fields = '__all__'


class ProduccionPorPlantaSerializer(serializers.Serializer):
    planta = serializers.CharField(source='producto__planta__nombre')
    producto = serializers.CharField(source='producto__nombre')
    total_litros = serializers.IntegerField()