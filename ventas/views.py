import json, io
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test

from django.db import transaction
from django.db.models import F

from .models import Producto
from .forms import ProductoForm
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa




# =========================================================
# 1) FUNCIÓN DE PERMISO PARA STAFF
# =========================================================
def es_staff(user):
    """
    Devuelve True solo si:
    - el usuario está autenticado
    - y además es staff (admin)
    Esto se usa en @user_passes_test para restringir vistas.
    """
    return user.is_authenticated and user.is_staff


# =========================================================
# 2) LISTA DE PRODUCTOS (PÁGINA VENTAS)
# =========================================================
def lista_productos(request):
    """
    Muestra todos los productos en la plantilla ventas.html.
    """
    productos = Producto.objects.all()
    return render(request, "ventas.html", {"productos": productos})


# =========================================================
# 3) CREAR PRODUCTO (SOLO STAFF)
# =========================================================
@user_passes_test(es_staff)
def crear_producto(request):
    """
    Permite cargar productos nuevos usando ProductoForm.
    - GET: muestra form vacío
    - POST: valida y guarda en BD
    """
    if request.method == "POST":
        # request.FILES permite subir imágenes/archivos del producto
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
    else:
        form = ProductoForm()

    return render(request, "crear_producto.html", {"form": form})


# =========================================================
# 4) CONFIRMAR COMPRA (DESCONTAR STOCK SEGURAMENTE)
# =========================================================
@transaction.atomic
def confirmar_compra(request):
    # 1) Aceptamos SOLO POST
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

    # 2) Intentamos leer el JSON del body
    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)

    carrito = data.get("carrito", [])

    # 3) Validación básica: carrito no vacío y formato correcto
    if not isinstance(carrito, list) or len(carrito) == 0:
        return JsonResponse({"success": False, "error": "Carrito vacío o inválido"}, status=400)

    # 4) Normalizamos/validamos items: id y cantidad
    #    También consolidamos por si viene el mismo producto repetido:
    #    Ej: [{id:1,cantidad:1},{id:1,cantidad:2}] => id1 total 3
    cantidades_por_id = {}
    for item in carrito:
        if not isinstance(item, dict):
            return JsonResponse({"success": False, "error": "Formato de carrito inválido"}, status=400)

        if "id" not in item or "cantidad" not in item:
            return JsonResponse({"success": False, "error": "Faltan campos id/cantidad"}, status=400)

        try:
            prod_id = int(item["id"])
            cant = int(item["cantidad"])
        except (ValueError, TypeError):
            return JsonResponse({"success": False, "error": "id/cantidad deben ser números"}, status=400)

        if prod_id <= 0:
            return JsonResponse({"success": False, "error": "id de producto inválido"}, status=400)

        if cant <= 0:
            return JsonResponse({"success": False, "error": "La cantidad debe ser mayor a 0"}, status=400)

        cantidades_por_id[prod_id] = cantidades_por_id.get(prod_id, 0) + cant

    ids = list(cantidades_por_id.keys())

    # 5) Traemos TODOS los productos involucrados de una sola vez
    #    y BLOQUEAMOS las filas para evitar compras simultáneas rompiendo stock.
    productos_qs = Producto.objects.select_for_update().filter(id__in=ids)

    # Convertimos a dict para acceso rápido por id
    productos_map = {p.id: p for p in productos_qs}

    # 6) Validación: que existan todos los productos del carrito
    faltantes = [pid for pid in ids if pid not in productos_map]
    if faltantes:
        return JsonResponse(
            {"success": False, "error": f"Producto(s) no existe(n): {faltantes}"},
            status=404
        )

    # 7) Validación de stock: primero verificamos TODO.
    #    Si algo no alcanza, no descontamos nada.
    for pid, cant in cantidades_por_id.items():
        p = productos_map[pid]
        if p.stock < cant:
            return JsonResponse(
                {"success": False, "error": f"No hay suficiente stock de {p.nombre}"},
                status=409
            )

    # 8) Descontar stock de forma segura usando F()
    for pid, cant in cantidades_por_id.items():
        Producto.objects.filter(id=pid).update(stock=F("stock") - cant)

    # --- NUEVA PARTE: ENVÍO DE FACTURA ---
    # 9) Preparamos la lista de productos para el email con nombres y precios
    if request.user.is_authenticated:
        carrito_para_email = []
        for pid, cant in cantidades_por_id.items():
            p = productos_map[pid]
            carrito_para_email.append({
                'nombre': p.nombre,
                'precio': p.precio,
                'cantidad': cant
            })
        
        # Intentamos enviar el mail
        try:
            # LLAMAMOS a la función enviándole el usuario actual y el carrito procesado
            enviar_factura_pdf(request.user, carrito_para_email)
        except Exception as e:
            print(f"Error al enviar factura: {e}") 

    # 10) Si llegamos acá, todo ok
    return JsonResponse({"success": True})


# VISTA PARA EDITAR
def editar_producto(request, producto_id):
    # Buscamos el producto o tiramos error 404 si no existe
    producto = get_object_or_404(Producto, pk=producto_id)
    
    if request.method == 'POST':
        # Pasamos los datos del POST y la instancia del producto actual
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos') # Volvemos a la lista de productos
    else:
        # Cargamos el formulario con los datos actuales del producto
        form = ProductoForm(instance=producto)
    
    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})

# VISTA PARA ELIMINAR
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    
    if request.method == 'POST':
        producto.delete() # Borramos de la base de datos
        return redirect('lista_productos')
        
    return render(request, 'confirmar_eliminar_prod.html', {'producto': producto})


def enviar_factura_pdf(user, carrito_data):
    # 1. Calculamos totales
    total = sum(item['precio'] * item['cantidad'] for item in carrito_data)
    for item in carrito_data:
        item['subtotal'] = item['precio'] * item['cantidad']

    # 2. Renderizamos el HTML del PDF
    template = get_template('factura_pdf.html')
    contexto = {'usuario': user, 'carrito': carrito_data, 'total': total}
    html = template.render(contexto)

    # 3. Creamos el PDF en memoria
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        # 4. Creamos el Email
        email = EmailMessage(
            f"Factura de Compra - Agus_Cardetail",
            f"Hola {user.username}, adjuntamos la factura de tu compra. ¡Gracias!",
            'aguspronahu11@gmail.com', # Tu mail configurado
            [user.email if user.email else 'paezagustinnahuel@gmail.com'],
        )
        
        # Adjuntamos el PDF generado
        email.attach(f'factura_{user.username}.pdf', result.getvalue(), 'application/pdf')
        email.send()
        print("✅ PDF generado y enviado con éxito.")