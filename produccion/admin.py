from datetime import timezone
from django.contrib import admin

from produccion.models import Planta, Producto
from .models import RegistroProduccion

class RegistroProduccionAdmin(admin.ModelAdmin):
    list_display = ('producto', 'litros', 'fecha', 'turno', 'operador', 'eliminado')
    actions = ['eliminar_registros']

    def eliminar_registros(self, request, queryset):
        queryset.update(eliminado=True, modificado_por=request.user, modificado_en=timezone.now())

    eliminar_registros.short_description = "Eliminar registros seleccionados"

admin.site.register(RegistroProduccion, RegistroProduccionAdmin)



admin.site.register(Planta)
admin.site.register(Producto)
