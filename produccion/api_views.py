from rest_framework.response import Response
from django.db.models import Sum
from rest_framework import generics
from .models import RegistroProduccion
from .serializers import ProduccionPorPlantaSerializer, RegistroProduccionSerializer
from .filters import RegistroProduccionFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.safestring import mark_safe
from .utils import send_slack_message
from rest_framework.permissions import IsAuthenticated

class RegistroProduccionListCreate(generics.ListCreateAPIView):#generics.ListCreateAPIView: Proporciona la funcionalidad para listar (GET) y crear (POST) objetos.
    queryset = RegistroProduccion.objects.all()
    serializer_class = RegistroProduccionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegistroProduccionFilter#Define la clase de filtros que se utilizará para aplicar filtros a las consultas, en este caso el filtro eprsonalizado que definimos
    permission_classes = [IsAuthenticated]

    def get_view_name(self):
        return "Lista y Creación de Producción"

    def get_view_description(self, html=False):
        description = (
            "Esta vista permite listar y crear registros de producción. "
            "Para ver el total de producción por planta, visite "
            '<a href="http://127.0.0.1:8000/produccion/api/produccion/total_por_planta/">'
            "Producción por Planta</a>."
        )
        return mark_safe(description)
    
    #Método sobrescrito para personalizar el comportamiento al crear un nuevo registro de producción. Asigna el usuario actual como operador y envía un mensaje a Slack usando una función utilitaria send_slack_message

    def perform_create(self, serializer):
        instance = serializer.save(operador=self.request.user)
        send_slack_message(instance)

class RegistroProduccionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegistroProduccion.objects.all()
    serializer_class = RegistroProduccionSerializer

    def get_view_name(self):
        return "Detalle, Actualización y Eliminación de Producción"

    def get_view_description(self, html=False):
        return "Esta vista permite recuperar, actualizar y eliminar registros de producción."


class ProduccionPorPlantaList(generics.GenericAPIView):#generics.GenericAPIView: Una vista base que proporciona las funcionalidades básicas de una vista genérica sin métodos concretos.
    serializer_class = ProduccionPorPlantaSerializer
    queryset = RegistroProduccion.objects.none()  # Añadir un queryset vacío

    def get(self, request, *args, **kwargs):
        queryset = RegistroProduccion.objects.values( #Values devuelve un diccionario de los valores especificados en lugar de instancias de modelo. En este caso, se están seleccionando los nombres de la planta (producto__planta__nombre) y del producto (producto__nombre).
            'producto__planta__nombre', 'producto__nombre'
        ).annotate(
            total_litros=Sum('litros')
        ).order_by(
            'producto__planta__nombre', 'producto__nombre'
        )

        serializer = self.get_serializer(queryset, many=True)#Los resultados de la consulta se pasan al serializer ProduccionPorPlantaSerializer, que convierte los datos en un formato que puede ser convertido a JSON. El serializer se encarga de convertir los datos del queryset en un formato que puede ser convertido a JSON y enviado como respuesta.
        return Response(serializer.data)