import django_filters
from .models import RegistroProduccion

class RegistroProduccionFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='fecha', lookup_expr='year')
    month = django_filters.NumberFilter(field_name='fecha', lookup_expr='month')

    class Meta:
        model = RegistroProduccion
        fields = ['producto__planta', 'year', 'month']
