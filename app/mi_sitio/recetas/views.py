from django.shortcuts import render, HttpResponse
from django.template import loader

# Create your views here.

def index(request):
    context = dict()
    return render(request, 'recetas/index.html', context)