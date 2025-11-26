# turnos/urls.py
from django.urls import path
from .views import turnos_view

urlpatterns = [
    path('', turnos_view, name='turnos'),
]
