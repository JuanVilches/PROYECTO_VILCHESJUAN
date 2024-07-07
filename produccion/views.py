from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import RegistroProduccion
from .forms import RegistroProduccionForm
from django.utils import timezone

@login_required
def registrar_produccion(request):
    if request.method == 'POST':
        form = RegistroProduccionForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.operador = request.user
            registro.save()
            return redirect('produccion:lista_produccion')
    else:
        form = RegistroProduccionForm()
    return render(request, 'produccion/registrar_produccion.html', {'form': form})

@login_required
def editar_produccion(request, pk):
    registro = get_object_or_404(RegistroProduccion, pk=pk, operador=request.user)
    if request.method == 'POST':
        form = RegistroProduccionForm(request.POST, instance=registro)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.modificado_por = request.user
            registro.modificado_en = timezone.now()
            registro.save()
            return redirect('produccion:lista_produccion')
    else:
        form = RegistroProduccionForm(instance=registro)
    return render(request, 'produccion/editar_produccion.html', {'form': form})

@login_required
def lista_produccion(request):
    registros = RegistroProduccion.objects.filter(operador=request.user, eliminado=False)
    return render(request, 'produccion/lista_produccion.html', {'registros': registros})
