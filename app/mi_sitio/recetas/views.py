from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.db.models import Q

from .models import Receta, Ingrediente
# Create your views here.

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


def receta_detalle(request, slug):
    receta = get_object_or_404(Receta, slug=slug)
    ingredientes = Ingrediente.objects.filter(receta=receta)
    context = {"receta": receta, "ingredientes": ingredientes}

    return render(request, "recetas/receta.html", context)