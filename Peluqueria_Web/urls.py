# Peluqueria_Web/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from turnos.views import inicio, logout_view
from django.conf import settings             # <--- IMPORTANTE: Agrega esto
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Inicio en "/"
    path('', inicio, name='inicio'),

    # Rutas de la app turnos (crean /turnos/, /turnos/<id>/editar, etc.)
    path('', include('turnos.urls')),

    # Login
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'
    ),
    path('ventas/', include('ventas.urls')),

    # Logout simple
    path('logout/', logout_view, name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
