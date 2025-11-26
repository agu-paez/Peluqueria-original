from django.urls import path
from . import views

urlpatterns = [
    path('', views.turnos_view, name='turnos'),
    path('turno/<int:turno_id>/editar/', views.editar_turno, name='editar_turno'),
    path('turno/<int:turno_id>/eliminar/', views.eliminar_turno, name='eliminar_turno'),
]
