from rest_framework.response import Response 
from django.db.models import Sum
from rest_framework import generics
from .models import RegistroProduccion
from .serializers import ProduccionPorPlantaSerializer, RegistroProduccionSerializer
from .filters import RegistroProduccionFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.safestring import mark_safe

class RegistroProduccionListCreate(generics.ListCreateAPIView):
    queryset = RegistroProduccion.objects.all()
    serializer_class = RegistroProduccionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegistroProduccionFilter

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

class RegistroProduccionRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = RegistroProduccion.objects.all()
    serializer_class = RegistroProduccionSerializer

    def get_view_name(self):
        return "Detalle, Actualización y Eliminación de Producción"

    def get_view_description(self, html=False):
        return "Esta vista permite recuperar, actualizar y eliminar registros de producción."


class ProduccionPorPlantaList(generics.GenericAPIView):
    serializer_class = ProduccionPorPlantaSerializer
    queryset = RegistroProduccion.objects.none()  # Añadir un queryset vacío

    def get(self, request, *args, **kwargs):
        queryset = RegistroProduccion.objects.values(
            'producto__planta__nombre', 'producto__nombre'
        ).annotate(
            total_litros=Sum('litros')
        ).order_by(
            'producto__planta__nombre', 'producto__nombre'
        )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)