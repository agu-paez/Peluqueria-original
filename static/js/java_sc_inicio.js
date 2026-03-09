const modal = document.getElementById("imageModal");
const fullImg = document.getElementById("fullImage");
const closeBtn = document.querySelector(".close-modal");

// 1. Buscamos todas las imágenes de las tarjetas
document.querySelectorAll(".card img").forEach(img => {
  img.addEventListener("click", () => {
    modal.style.display = "flex"; // Mostramos el modal
    setTimeout(() => modal.classList.add("active"), 10); // Animación de entrada
    fullImg.src = img.src; // Le pasamos la ruta de la imagen clickeada
  });
});

// 2. Función para cerrar el modal
const closeModal = () => {
  modal.classList.remove("active");
  setTimeout(() => modal.style.display = "none", 300);
};

closeBtn.addEventListener("click", closeModal);

// 3. Cerrar si hacen click afuera de la imagen
modal.addEventListener("click", (e) => {
  if (e.target === modal) closeModal();
});
