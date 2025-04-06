from django.shortcuts import render, redirect, get_object_or_404
from .models import Cita
from .forms import CitaForm

def lista_citas(request):
    citas = Cita.objects.all().order_by('-fecha', '-hora')
    return render(request, 'pacientes/lista_citas.html', {'citas': citas})

def agregar_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_citas')
    else:
        form = CitaForm()
    return render(request, 'pacientes/agregar_cita.html', {'form': form})

def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            return redirect('lista_citas')
    else:
        form = CitaForm(instance=cita)
    return render(request, 'pacientes/editar_cita.html', {'form': form, 'cita': cita})

def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    if request.method == 'POST':
        cita.delete()
        return redirect('lista_citas')
    return render(request, 'pacientes/eliminar_cita.html', {'cita': cita})