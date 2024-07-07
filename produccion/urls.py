from django.urls import path
from . import views

app_name = 'produccion'

urlpatterns = [
    path('', views.lista_produccion, name='lista_produccion'),
    path('registrar/', views.registrar_produccion, name='registrar_produccion'),
    path('editar/<int:pk>/', views.editar_produccion, name='editar_produccion'),
]
