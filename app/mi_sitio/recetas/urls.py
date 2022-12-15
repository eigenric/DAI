# recetas/urls.py
from django.urls import path
from .views import index, receta_detalle, change_theme, receta_new


urlpatterns = [
    path('', index, name='index'),
    path('crear-receta', receta_new, name="crear_receta"),
    path('receta/<slug:slug>', receta_detalle, name="receta_detalle"),
    path('change-theme', change_theme, name='change_theme')
]