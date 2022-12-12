# recetas/urls.py
from django.urls import path
from .views import receta_detalle

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('receta/<slug:slug>', receta_detalle, name="unique_slug"),
]