from django.contrib import admin
from .models import Evento, Categoria, Avaliacao, Comentario

admin.site.register(Evento)
admin.site.register(Categoria)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento', 'texto', 'data_criacao') # Colunas que aparecem na lista
    list_filter = ('evento', 'data_criacao') # Filtros laterais
    search_fields = ('texto', 'usuario__username') # Barra de busca