# turnos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # página de turnos
    path('turnos/', views.turnos_view, name='turnos'),

    # editar / eliminar turno (para los botones del modal)
    path('turnos/<int:turno_id>/editar/', views.editar_turno, name='editar_turno'),
    path('turnos/<int:turno_id>/eliminar/', views.eliminar_turno, name='eliminar_turno'),
]
