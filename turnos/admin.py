from django.contrib import admin
from .models import Turnos

@admin.register(Turnos)
class TurnosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha','hora','sena')
    list_filter = ('fecha',)
    search_fields = ('nombre',)
