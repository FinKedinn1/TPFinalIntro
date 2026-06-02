// Configuración del Backend (puedes cambiar este puerto por el de tu API)
const BACKEND_URL = 'http://localhost:5000/api/menu';
const Platos = document.getElementsByClassName('carta-de-platos');
const Botones = document.getElementsByClassName("boton-filtrar");
    for (let i = 0; i < Botones.length; i++) {
        Botones[i].addEventListener("click", function() {
            for (let j = 0; j < Botones.length; j++) {
                Botones[j].classList.remove("activo");
            }
            Botones[i].classList.add("activo");
            const categoria_seleccionada = Botones[i].dataset.filter;

            for (let k = 0; k < Platos.length; k++) {
                const plato = Platos[k];
                const categoria_plato = plato.getAttribute("comida-categoria");

                if (categoria_seleccionada === "all") {
                    plato.classList.remove("comida-escondida");
                } else {
                    if (categoria_plato === categoria_seleccionada) {
                        plato.classList.remove("comida-escondida");
                    } else {
                        plato.classList.add("comida-escondida");
                    }
                }
            }

        }); 
    }


// Renderiza las tarjetas del menú
function renderizarPlatos(platos, container) {
    container.innerHTML = '';
    
    if (platos.length === 0) {
        container.innerHTML = `<p style="grid-column: 1/-1; text-align: center; font-style: italic; color: var(--text-dim);">No hay platos disponibles en este momento.</p>`;
        return;
    }

    platos.forEach(plato => {
        const card = document.createElement('div');
        card.className = 'card';
        card.setAttribute('data-category', normalizeCategory(plato.categoria));

        // Formatear precio
        const formattedPrice = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', minimumFractionDigits: 0 }).format(plato.precio);

        card.innerHTML = `
            ${plato.popular ? `<div class="badge-popular">Popular</div>` : ''}
            <div class="card-img-container">
                <img src="${plato.imagen}" alt="${plato.nombre}" onerror="this.src='https://images.unsplash.com/photo-1514933651103-005eec06c04b?q=80&w=1200'">
            </div>
            <div class="card-content">
                <h3>${plato.nombre}</h3>
                <p class="card-description">${plato.descripcion}</p>
                <div class="card-info">
                    <p class="card-category"><strong>Categoría:</strong> ${plato.categoria}</p>
                    <div class="card-price-container">
                        <span class="card-price">${formattedPrice}</span>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(card);
    });
}


// Configuración de los botones de filtros
function configurarFiltros() {
    const buttons = document.querySelectorAll('.filter-btn');

    buttons.forEach(button => {
        button.addEventListener('click', () => {
            // Quitar clase activa
            buttons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const categoryFilter = button.getAttribute('data-filter');
            const cards = document.querySelectorAll('.card');

            cards.forEach(card => {
                const cardCategory = card.getAttribute('data-category');
                
                if (categoryFilter === 'all') {
                    card.classList.remove('hidden');
                } else {
                    const normalizedFilter = normalizeCategory(categoryFilter);
                    if (cardCategory === normalizedFilter) {
                        card.classList.remove('hidden');
                    } else {
                        card.classList.add('hidden');
                    }
                }
            });
        });
    });
}

