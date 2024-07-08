from rest_framework import serializers
from .models import RegistroProduccion,Producto, User

class RegistroProduccionSerializer(serializers.ModelSerializer):
    producto = serializers.SlugRelatedField(slug_field='nombre', queryset=Producto.objects.all())#SlugRelatedField es un campo de serializador que permite representar una relación con otro modelo utilizando un campo específico (el "slug field") del modelo relacionado, en lugar de utilizar la clave primaria (ID).
    operador = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), required=False)
    modificado_por = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), required=False)

    class Meta:
        model = RegistroProduccion
        fields = '__all__'


class ProduccionPorPlantaSerializer(serializers.Serializer):
    planta = serializers.CharField(source='producto__planta__nombre')#source='producto__planta__nombre': Indica que el valor del campo planta debe obtenerse navegando desde el producto relacionado, luego a través de la relación planta, y finalmente obteniendo el valor del campo nombre en Planta.
    producto = serializers.CharField(source='producto__nombre')
    total_litros = serializers.IntegerField()