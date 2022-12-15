from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.db.models import Q

from .models import Receta, Ingrediente
from .forms import RecetaForm

import logging

def index(request):
    
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
    if request.session["theme"] == "light":
        request.session["theme"] = "dark"
    else:
        request.session["theme"] = "light"

    return index(request)

def receta_detalle(request, slug):
    receta = get_object_or_404(Receta, slug=slug)
    ingredientes = Ingrediente.objects.filter(receta=receta)
    context = {"receta": receta, "ingredientes": ingredientes}

    return render(request, "recetas/receta.html", context)

def receta_new(request):
    print("creado formulario")
    form = RecetaForm()
    print("Estoy en la vista")

    if request.method == "POST":
        form = RecetaForm(request.POST)
        if form.is_valid():
            receta = form.save(commit=False)
            receta.save()
            return redirect('receta_detalle', slug=receta.slug)
    else:
        form = RecetaForm()
    return render(request, "recetas/receta_edit.html", {'form': form})