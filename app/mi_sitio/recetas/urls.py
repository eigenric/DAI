# recetas/urls.py
from django.urls import path, include
from .views import index, receta_detalle, change_theme, receta_new, receta_delete, receta_edit


urlpatterns = [
    path('', index, name='index'),
    path('crear-receta', receta_new, name="crear_receta"),
    path('eliminar-receta/<slug:slug>', receta_delete, name="receta_delete"),       
    path('receta/<slug:slug>', receta_detalle, name="receta_detalle"),
    path('editar-receta/<slug:slug>', receta_edit, name="receta_edit"),
    path('change-theme', change_theme, name='change_theme'),
]