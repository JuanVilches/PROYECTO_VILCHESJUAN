from django.urls import path

from produccion import api_views
from . import views

app_name = 'produccion'

urlpatterns = [
    path('', views.lista_produccion, name='lista_produccion'),
    path('registrar/', views.registrar_produccion, name='registrar_produccion'),
    path('editar/<int:pk>/', views.editar_produccion, name='editar_produccion'),
    path('api/produccion/', api_views.RegistroProduccionListCreate.as_view(), name='api_produccion_list_create'),
    path('api/produccion/<int:pk>/', api_views.RegistroProduccionRetrieveUpdateDestroy.as_view(), name='api_produccion_rud'),
    path('api/produccion/total_por_planta/', api_views.ProduccionPorPlantaList.as_view(), name='api_produccion_total_por_planta'),
]
