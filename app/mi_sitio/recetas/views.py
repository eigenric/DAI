from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.db.models import Q
from django.contrib import messages

from .models import Receta, Ingrediente
from .forms import RecetaForm

import logging


MESSAGE_TAGS = {
    messages.SUCCESS: 'success',
}


def index(request):
    """Pagina principal. Listado de recetas buscadas o de todas las recetas"""
    
    search_post = request.GET.get('search')
    if search_post:
        recetas = Receta.objects.filter(
            Q(nombre__icontains=search_post) | Q(preparación__icontains=search_post)
        )
        template = 'recetas/search.html'
    else:
        recetas = Receta.objects.all()
        template = 'recetas/index.html'
    context = {"recetas": recetas}
        
    return render(request, template, context)

def change_theme(request):
    """Manejo de sesiones para el cambio de tema oscuro o claro """

    if not "theme" in request.session:
        request.session["theme"] = "light"

    if request.session["theme"] == "light":
        request.session["theme"] = "dark"
    else:
        request.session["theme"] = "light"

    return index(request)

def receta_detalle(request, slug):
    """Visualización del detalle de cada receta"""

    receta = get_object_or_404(Receta, slug=slug)
    ingredientes = Ingrediente.objects.filter(receta=receta)
    context = {"receta": receta, "ingredientes": ingredientes}

    return render(request, "recetas/receta.html", context)


def receta_delete(request, slug):
    """Eliminar una receta de la base de datos"""

    receta = Receta.objects.get(slug=slug)
    receta.delete()
    messages.success(request, "Receta eliminada satisfactoriamente")

    return index(request)


def receta_new(request):
    """
    Creación de nueva receta por formulario de django. 
    Uso de crispy-forms
    Con extensión en boostrap 5.
    """

    if request.method == "POST":
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            receta = Receta(nombre=request.POST["nombre"],
                            preparación=request.POST["preparación"],
                            foto=request.FILES["foto"])
            receta.save()
            messages.success(request, "Receta creada satisfactoriamente")
            return redirect('receta_detalle', slug=receta.slug)
    else:
        form = RecetaForm()

    return render(request, "recetas/receta_edit.html", {'form': form})

def receta_edit(request, slug):
    """Formulario para editar una receta de la base de datos."""

    receta = get_object_or_404(Receta, slug=slug)
    if request.method == "POST":
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            receta.nombre=request.POST["nombre"]
            receta.preparación = request.POST["preparación"]
            receta.foto = request.FILES["foto"]
            receta.save()
            messages.success(request, "Receta editada satisfactoriamente")
            return redirect('receta_detalle', slug=receta.slug)
    else:
        form = RecetaForm(instance=receta)
    return render(request, 'recetas/receta_edit.html', {'form': form})