from django.shortcuts import render, get_object_or_404
from django.template import loader
from .models import Receta, Ingrediente
# Create your views here.

def index(request):
    recetas = Receta.objects.all()
    context = {"recetas": recetas}
    return render(request, 'recetas/index.html', context)

def receta_detalle(request, slug):
    receta = get_object_or_404(Receta, slug=slug)
    ingredientes = Ingrediente.objects.filter(receta=receta)
    context = {"receta": receta, "ingredientes": ingredientes}

    return render(request, "recetas/receta.html", context)