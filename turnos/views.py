from datetime import date
import calendar
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.contrib.auth import logout

from .models import Turnos
from .forms import TurnoForm


# ✅ Esta función se usa como "filtro" para permitir acceso solo a staff autenticado.
def es_staff(user):
    return user.is_authenticated and user.is_staff


# ✅ Lista para mostrar el nombre del mes en español.
# Pone un string vacío en la posición 0 para que:
# MESES_ES[1] = "Enero", MESES_ES[2] = "Febrero", etc.
MESES_ES = [
    "",
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]


# ✅ Vista simple que solo renderiza el inicio.
def inicio(request):
    return render(request, "inicio.html")


def turnos_view(request):
    # ✅ Fecha de hoy (del sistema)
    hoy = date.today()

    # ✅ Lee year y month desde la URL:
    # /turnos/?year=2026&month=2
    # Si no vienen, usa el año/mes actual.
    year = int(request.GET.get("year", hoy.year))
    month = int(request.GET.get("month", hoy.month))

    # ✅ Calcular mes anterior (para botón “←”)
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    # ✅ Calcular mes siguiente (para botón “→”)
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    # ✅ Permiso: solo si está logueado y es staff
    puede_editar = request.user.is_authenticated and request.user.is_staff

    # ------------------------------
    # ✅ Manejo del formulario (crear turno)
    # ------------------------------
    if request.method == 'POST':
        # Si alguien que NO es staff intenta mandar POST (crear turno),
        # lo rebotás y lo mandás de nuevo al calendario.
        if not puede_editar:
            return redirect(f"{reverse('turnos')}?year={year}&month={month}")

        # Crea el formulario con los datos del POST (lo que viene del HTML)
        form = TurnoForm(request.POST)

        # Si los datos cumplen validaciones del form/model:
        if form.is_valid():
            form.save()  # Guarda el turno en la base de datos
            # Y vuelve al mismo calendario del mes actual
            return redirect(f"{reverse('turnos')}?year={year}&month={month}")
    else:
        # Si es GET, mostrás el formulario vacío
        form = TurnoForm()

    # ------------------------------
    # ✅ Armar calendario (estructura semanas/días)
    # ------------------------------
    # calendar.monthcalendar(year, month) devuelve una lista de semanas,
    # y cada semana es una lista de 7 números:
    # - 0 significa "ese día no pertenece al mes" (relleno)
    # - 1..31 son los días reales del mes
    cal = calendar.monthcalendar(year, month)

    weeks = []  # acá guardamos el calendario "procesado" para la plantilla
    for week in cal:
        week_days = []
        for day in week:
            if day == 0:
                # Día vacío en el calendario (antes del 1 o después del último día)
                week_days.append(None)
            else:
                # Convertimos el número de día en un objeto date real
                d = date(year, month, day)
                # Guardamos info útil para el template/JS
                week_days.append({
                    'num': day,                        # número visible (1..31)
                    'date': d.strftime('%Y-%m-%d'),    # "2026-02-20" para usar como clave/HTML
                })
        weeks.append(week_days)

    # ------------------------------
    # ✅ Turnos del mes (consulta a la base de datos)
    # ------------------------------
    turnos_qs = Turnos.objects.filter(
        fecha__year=year,
        fecha__month=month
    ).order_by('fecha', 'hora')  # ordenados por fecha y hora

    # ------------------------------
    # ✅ Agrupar turnos por día (diccionario)
    # ------------------------------
    # Queda algo así:
    # {
    #   "2026-02-20": [turno1, turno2],
    #   "2026-02-21": [turno3]
    # }
    turnos_por_dia = {}

    for t in turnos_qs:
        clave = t.fecha.strftime('%Y-%m-%d')

        # ✅ Si es staff, mandás datos completos (privados)
        if request.user.is_authenticated and request.user.is_staff:
            datos_turno = {
                'id': t.id,
                'hora': t.hora.strftime('%H:%M'),
                'nombre': t.nombre,
                'desc': t.desc or '',  # si desc es None, mandás string vacío
                'sena': float(t.sena), # para que JSON no falle con Decimal
                'editar_url': reverse('editar_turno', args=[t.id]),
                'eliminar_url': reverse('eliminar_turno', args=[t.id]),
            }
        else:
            # ✅ Si NO es staff: no mandás información sensible.
            # Solo mandás algo para que el JS sepa que “hay un turno” y cuente cantidad.
            datos_turno = { 'privado': True }

        # setdefault crea la lista si no existe y después le hace append
        turnos_por_dia.setdefault(clave, []).append(datos_turno)

    # ✅ Convertís el diccionario a JSON para usarlo en JavaScript en el template
    turnos_json = json.dumps(turnos_por_dia)

    # ------------------------------
    # ✅ Contexto para el template turnos.html
    # ------------------------------
    context = {
        'year': year,
        'month': month,
        'month_name': MESES_ES[month],
        'weeks': weeks,
        'form': form,
        'turnos_json': turnos_json,

        # para botones de navegación del calendario
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,

        # permiso en el template (mostrar botones / formulario)
        'puede_editar': puede_editar,

        # queryset completo del mes (por si lo querés usar en el template)
        'turnos_mes': turnos_qs,
    }

    return render(request, 'turnos.html', context)


# ✅ Decorador: solo deja entrar si es_staff(user) devuelve True
@user_passes_test(es_staff)
def editar_turno(request, turno_id):
    # Busca el turno por id. Si no existe, 404.
    turno = get_object_or_404(Turnos, pk=turno_id)

    if request.method == 'POST':
        # instance=turno significa: editar este registro, no crear uno nuevo
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            # volver al calendario del mismo mes del turno
            year = turno.fecha.year
            month = turno.fecha.month
            return redirect(f"{reverse('turnos')}?year={year}&month={month}")
    else:
        # GET: mostrar formulario precargado con datos del turno
        form = TurnoForm(instance=turno)

    return render(request, 'editar_turno.html', {
        'form': form,
        'turno': turno,
    })


@user_passes_test(es_staff)
def eliminar_turno(request, turno_id):
    turno = get_object_or_404(Turnos, pk=turno_id)

    if request.method == 'POST':
        # Guardás año/mes ANTES de borrar para volver al calendario correcto
        year = turno.fecha.year
        month = turno.fecha.month
        turno.delete()
        return redirect(f"{reverse('turnos')}?year={year}&month={month}")

    # GET: mostrar pantalla de confirmación
    return render(request, 'confirmar_eliminar.html', {
        'turno': turno,
    })


def logout_view(request):
    # Cierra la sesión del usuario
    logout(request)

    # Intenta volver a:
    # 1) ?next=...
    # 2) página anterior (HTTP_REFERER)
    # 3) o a inicio
    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or reverse('inicio')
    return redirect(next_url)