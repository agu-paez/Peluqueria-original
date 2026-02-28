// --- JAVASCRIPT PELUQUERÍA IVON (CON LÓGICA VISUAL DE STOCK) ---

let carrito = JSON.parse(localStorage.getItem("carrito_peluqueria")) || [];

const guardarLocal = () => {
    localStorage.setItem("carrito_peluqueria", JSON.stringify(carrito));
};

const total_Ul = () => {
    const totalUnidades = carrito.reduce((acc, p) => acc + p.cantidad, 0);
    const contador = document.getElementById("contador-carrito");
    if (contador) contador.innerText = totalUnidades; 
};

// --- NUEVA FUNCIÓN MÁGICA: Actualiza la tarjeta visualmente ---
const actualizarStockVisual = (id, stockMaximo) => {
    // 1. Buscamos los elementos HTML por su ID único
    const textoStock = document.getElementById(`stock-texto-${id}`);
    const btnAgregar = document.getElementById(`btn-agregar-${id}`);

    if (!textoStock || !btnAgregar) return; // Si no existen, salimos

    // 2. Calculamos cuánto queda realmente PARA ESTE USUARIO
    const productoEnCarrito = carrito.find(p => p.id === id);
    const cantidadEnCarrito = productoEnCarrito ? productoEnCarrito.cantidad : 0;
    const stockRestante = stockMaximo - cantidadEnCarrito;

    // 3. Modificamos el DOM según el resultado
    if (stockRestante <= 0) {
        // CASO: AGOTADO (Lo ponemos rojo y bloqueamos)
        textoStock.innerHTML = '<span style="color: red;">🚫 AGOTADO </span>';
        btnAgregar.innerText = "Sin Stock";
        btnAgregar.disabled = true;
        btnAgregar.style.backgroundColor = "#ccc";
        btnAgregar.style.cursor = "not-allowed";
    } else if (stockRestante === 1) {
        // CASO: ÚLTIMA UNIDAD
        textoStock.innerHTML = '<span style="color: orange;">⚠️ ¡ÚLTIMA UNIDAD!</span>';
        btnAgregar.disabled = false;
        btnAgregar.innerText = "Agregar al Carrito";
        btnAgregar.style.backgroundColor = "#004289";
        btnAgregar.style.cursor = "pointer";
    } else {
        // CASO: NORMAL
        textoStock.innerText = `Stock disponible: ${stockRestante}`;
        btnAgregar.disabled = false;
        btnAgregar.innerText = "Agregar al Carrito";
        btnAgregar.style.backgroundColor = "#004289";
        btnAgregar.style.cursor = "pointer";
    }
};

const carrito_loading = () => {
    let cont_ventana = document.getElementById("ventana_carrito");
    let lista_carrito = document.getElementById("lista-carrito");
    
    lista_carrito.innerHTML = ""; 

    if (carrito.length === 0) {
        lista_carrito.innerHTML = "<p>El carrito está vacío.</p>";
    } else {
        carrito.forEach((p) => {
            let div_item = document.createElement("div");
            div_item.className = "lista_carrito";
            div_item.innerHTML = `
                <p><strong>${p.nombre}</strong> <br> ${p.cantidad} x $${p.precio}</p>
                <p>$${(p.precio * p.cantidad).toFixed(2)} <button class="btn-quitar" data-id="${p.id}"> X </button></p>
            `;
            lista_carrito.appendChild(div_item);
        });

        document.querySelectorAll(".btn-quitar").forEach(btn => {
            btn.onclick = (e) => eliminarProducto(parseInt(e.target.dataset.id));
        });

        const totalCompra = carrito.reduce((acu, p) => acu + (p.precio * p.cantidad), 0); 
        let div_total = document.createElement("div");
        div_total.innerHTML = `<hr><h3>Total Final: $${totalCompra.toFixed(2)}</h3>`;
        lista_carrito.appendChild(div_total);
    }
    cont_ventana.style.display = "block";
};

const eliminarProducto = (id) => {
    let producto = carrito.find((p) => p.id === id);
    if (producto) {
        if (producto.cantidad > 1) {
            producto.cantidad--; 
        } else {
            carrito = carrito.filter((p) => p.id !== id);
        }
        
        Toastify({
            text: `¡${producto.nombre.toUpperCase()} ELIMINADO!`,
            duration: 1000,
            gravity: "top", position: "right",
            style: { background: "#d9534f", borderRadius: "10px" }
        }).showToast();
    }
    
    guardarLocal(); 
    total_Ul();
    carrito_loading();
    
    // IMPORTANTE: Al eliminar, recuperamos el stock visualmente
    // Necesitamos buscar el botón original para saber el stock máximo real
    const btnOriginal = document.getElementById(`btn-agregar-${id}`);
    if (btnOriginal) {
        const stockMax = parseInt(btnOriginal.dataset.stock);
        actualizarStockVisual(id, stockMax);
    }
};

const limpiarCarrito = () => {
    Swal.fire({
        title: "¿Vaciar?", text: "Se eliminarán los productos.", icon: "warning",
        showCancelButton: true, confirmButtonText: "Sí", cancelButtonText: "No"
    }).then((result) => {
        if (result.isConfirmed) {
            // Guardamos IDs para restaurar stock visual antes de borrar
            const idsEnCarrito = carrito.map(p => p.id);
            
            carrito = []; 
            localStorage.removeItem("carrito_peluqueria"); 
            total_Ul(); 
            carrito_loading();
            document.getElementById("ventana_carrito").style.display = "none";

            // Restauramos visualmente todos los productos
            idsEnCarrito.forEach(id => {
                const btn = document.getElementById(`btn-agregar-${id}`);
                if (btn) actualizarStockVisual(id, parseInt(btn.dataset.stock));
            });

            Swal.fire("Vaciado", "", "success");
        } 
    });
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// --- EVENTOS ---
document.addEventListener("DOMContentLoaded", () => {
    const botonesAgregar = document.querySelectorAll(".btn_agregar");
    
    // 1. RECORREMOS BOTONES PARA INICIALIZAR ESTADO (Por si recargas la página)
    botonesAgregar.forEach(boton => {
        let id = parseInt(boton.dataset.id);
        let stockMax = parseInt(boton.dataset.stock);
        
        // Ejecutamos la validación visual al cargar la página
        actualizarStockVisual(id, stockMax);

        // 2. EVENTO CLICK
        boton.addEventListener("click", (e) => {
            let nombre = e.target.dataset.nombre;
            let precio = parseFloat(e.target.dataset.precio.replace(',', '.')); 
            if (isNaN(precio)) precio = 0;
            
            let productoEnCarrito = carrito.find(p => p.id === id);
            let cantidadEnCarrito = productoEnCarrito ? productoEnCarrito.cantidad : 0;

            if (cantidadEnCarrito < stockMax) { 
                if (productoEnCarrito) {
                    productoEnCarrito.cantidad++;
                } else {
                    carrito.push({ id, nombre, precio, cantidad: 1 });
                }
                guardarLocal();
                total_Ul();
                
                // ACTUALIZAMOS VISUALMENTE LA TARJETA INSTANTÁNEAMENTE
                actualizarStockVisual(id, stockMax);

                if (document.getElementById("ventana_carrito").style.display === "block") {
                    carrito_loading();
                }
                Toastify({
                    text: `¡${nombre.toUpperCase()} AGREGADO!`, duration: 2000, gravity: "top", position: "right",
                    style: { background: "linear-gradient(to right, #004289, #0072ff)", borderRadius: "10px" }
                }).showToast();
            }
        });
    });

    // Resto de botones
    document.getElementById("icon-carrito").addEventListener("click", () => {
        let v = document.getElementById("ventana_carrito");
        v.style.display = (v.style.display === "none" || v.style.display === "") ? "block" : "none";
        if (v.style.display === "block") carrito_loading();
    });

    document.getElementById("btn-cerrar").addEventListener("click", () => document.getElementById("ventana_carrito").style.display = "none");
    document.getElementById("btn-limpiar").addEventListener("click", limpiarCarrito);

    document.getElementById("btn-comprar").addEventListener("click", () => {
        if (carrito.length > 0) {
            Swal.fire({ title: 'Procesando...', willOpen: () => Swal.showLoading(), showConfirmButton: false });
            fetch('/ventas/confirmar_compra/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
                body: JSON.stringify({ 'carrito': carrito })
            })
            .then(r => r.json())
            .then(d => {
                if (d.success) {
                    Swal.fire('¡Éxito!', 'Compra realizada.', 'success').then(() => {
                        carrito = []; guardarLocal(); window.location.reload(); 
                    });
                } else {
                    Swal.fire('Error', d.error, 'error');
                }
            });
        } else {
            Swal.fire('Carrito vacío', '', 'warning');
        }
    });

    total_Ul();
});

eliminar_prod = getElementById("boton")