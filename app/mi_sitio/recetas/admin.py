from django.contrib import admin
from .models import Receta, Ingrediente

class RecetaAdmin(admin.ModelAdmin):
    pass

class IngredienteAdmin(admin.ModelAdmin):
    pass

admin.site.register(Receta, RecetaAdmin)
admin.site.register(Ingrediente, IngredienteAdmin)