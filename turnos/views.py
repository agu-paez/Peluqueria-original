from datetime import date
import calendar
import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test

from .models import Turnos
from .forms import TurnoForm

MESES_ES = [
    "",
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre"
]


def turnos_view(request):
    hoy = date.today()
    year = int(request.GET.get("year", hoy.year))
    month = int(request.GET.get("month", hoy.month))

    # calcular mes anterior y siguiente
    if month == 1:
        prev_month = 12
        prev_year = year - 1
    else:
        prev_month = month - 1
        prev_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    # solo puede cargar turnos si está logueada y es staff (tu mamá)
    puede_editar = request.user.is_authenticated and request.user.is_staff

    # Manejo del formulario (alta de turno)
    if request.method == 'POST':
        if not puede_editar:
            # Si no tiene permiso, ignoro el POST y redirijo
            return redirect(f"/?year={year}&month={month}")

        form = TurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f"/?year={year}&month={month}")
    else:
        form = TurnoForm()

    # Armar calendario (semanas y días)
    cal = calendar.monthcalendar(year, month)
    weeks = []
    for week in cal:
        week_days = []
        for day in week:
            if day == 0:
                week_days.append(None)
            else:
                d = date(year, month, day)
                week_days.append({
                    'num': day,
                    'date': d.strftime('%Y-%m-%d'),
                })
        weeks.append(week_days)

    # Turnos del mes
    turnos_qs = Turnos.objects.filter(
        fecha__year=year,
        fecha__month=month
    ).order_by('fecha', 'hora')

    turnos_por_dia = {}
    for t in turnos_qs:
        clave = t.fecha.strftime('%Y-%m-%d')
        turnos_por_dia.setdefault(clave, []).append({
            'hora': t.hora.strftime('%H:%M'),
            'nombre': t.nombre,
            'desc': t.desc or '',
            'sena': float(t.sena),
        })

    turnos_json = json.dumps(turnos_por_dia)

    context = {
        'year': year,
        'month': month,
        'month_name': MESES_ES[month],
        'weeks': weeks,
        'form': form,
        'turnos_json': turnos_json,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'puede_editar': puede_editar,
        'turnos_mes': turnos_qs,   # para la tabla de administración
    }
    return render(request, 'turnos.html', context)


# ======== PERMISOS PARA EDITAR / ELIMINAR (solo staff) =========

def es_staff(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(es_staff)
def editar_turno(request, turno_id):
    turno = get_object_or_404(Turnos, pk=turno_id)

    if request.method == 'POST':
        form = TurnoForm(request.POST, instance=turno)
        if form.is_valid():
            form.save()
            year = turno.fecha.year
            month = turno.fecha.month
            return redirect(f"/?year={year}&month={month}")
    else:
        form = TurnoForm(instance=turno)

    return render(request, 'editar_turno.html', {
        'form': form,
        'turno': turno,
    })


@user_passes_test(es_staff)
def eliminar_turno(request, turno_id):
    turno = get_object_or_404(Turnos, pk=turno_id)

    if request.method == 'POST':
        year = turno.fecha.year
        month = turno.fecha.month
        turno.delete()
        return redirect(f"/?year={year}&month={month}")

    return render(request, 'confirmar_eliminar.html', {
        'turno': turno,
    })

