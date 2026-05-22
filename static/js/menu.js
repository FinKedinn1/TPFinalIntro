// Configuración del Backend (puedes cambiar este puerto por el de tu API)
const BACKEND_URL = 'http://localhost:5000/api/menu';

// Base de datos local (Fallback/Offline) - Banquetes del Reino
const LOCAL_MENU = [
    {
        id: 1,
        nombre: "Hamburguesa del Rey",
        descripcion: "Hamburguesa saludable con pan integral.",
        categoria: "Plato Principal",
        precio: 8500,
        imagen: "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=1200&auto=format&fit=crop",
        popular: true
    },
    {
        id: 2,
        nombre: "Papas del Castillo",
        descripcion: "Papas rústicas con especias medievales.",
        categoria: "Entradas",
        precio: 4200,
        imagen: "https://images.unsplash.com/photo-1576107232684-1279f390859f?q=80&w=1200&auto=format&fit=crop",
        popular: false
    },
    {
        id: 3,
        nombre: "Poción Frutal",
        descripcion: "Jugo natural de frutos rojos.",
        categoria: "Bebidas",
        precio: 3000,
        imagen: "https://images.unsplash.com/photo-1544145945-f90425340c7e?q=80&w=1200&auto=format&fit=crop",
        popular: true
    },
    {
        id: 4,
        nombre: "Tarta del Guerrero",
        descripcion: "Tarta integral de manzana.",
        categoria: "Postres",
        precio: 3900,
        imagen: "https://images.unsplash.com/photo-1568571780765-9276ac8b75a2?q=80&w=1200&auto=format&fit=crop",
        popular: false
    },
    {
        id: 5,
        nombre: "Sandwich Saludable de Pollo",
        descripcion: "Sandwich integral con pollo grillado y vegetales frescos.",
        categoria: "Plato Principal",
        precio: 7800,
        imagen: "https://images.unsplash.com/photo-1525351484163-7529414344d8?q=80&w=1200&auto=format&fit=crop",
        popular: false
    },
    {
        id: 6,
        nombre: "Liebre al Escabeche",
        descripcion: "Liebre marinada con especias y vegetales medievales.",
        categoria: "Plato Principal",
        precio: 12500,
        imagen: "https://images.unsplash.com/photo-1600891964092-4316c288032e?q=80&w=1200&auto=format&fit=crop",
        popular: false
    },
    {
        id: 7,
        nombre: "Jabali al Ajillo",
        descripcion: "Jabali cocinado lentamente con ajo y hierbas.",
        categoria: "Plato Principal",
        precio: 14800,
        imagen: "https://images.unsplash.com/photo-1558030006-450675393462?q=80&w=1200&auto=format&fit=crop",
        popular: true
    },
    {
        id: 8,
        nombre: "Guiso de Pichon de Gorrion",
        descripcion: "Guiso espeso tradicional servido en cazuela de barro.",
        categoria: "Plato Principal",
        precio: 9200,
        imagen: "https://images.unsplash.com/photo-1547592180-85f173990554?q=80&w=1200&auto=format&fit=crop",
        popular: false
    },
    {
        id: 9,
        nombre: "Omelete de Huevo de Pato",
        descripcion: "Omelete cremoso con queso y hierbas del bosque.",
        categoria: "Entradas",
        precio: 6400,
        imagen: "https://images.unsplash.com/photo-1510693206972-df098062cb71?q=80&w=1200&auto=format&fit=crop",
        popular: false
    },
    {
        id: 10,
        nombre: "Pottage",
        descripcion: "Estofado medieval de verduras, legumbres y especias.",
        categoria: "Sopas",
        precio: 5900,
        imagen: "https://images.unsplash.com/photo-1547592166-23ac45744acd?q=80&w=1200&auto=format&fit=crop",
        popular: true
    },
    {
        id: 11,
        nombre: "Sopa de Cerveza y Pan Integral",
        descripcion: "Sopa caliente con cerveza negra artesanal y pan tostado.",
        categoria: "Sopas",
        precio: 5500,
        imagen: "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?q=80&w=1200&auto=format&fit=crop",
        popular: false
    },
    {
        id: 12,
        nombre: "Pasteles de Carne de Soja",
        descripcion: "Pasteles horneados rellenos de soja condimentada.",
        categoria: "Vegetariano",
        precio: 6700,
        imagen: "https://images.unsplash.com/photo-1509440159596-0249088772ff?q=80&w=1200&auto=format&fit=crop",
        popular: false
    },
    {
        id: 13,
        nombre: "Hidromiel",
        descripcion: "Bebida fermentada de miel al estilo vikingo.",
        categoria: "Bebidas",
        precio: 4800,
        imagen: "https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?q=80&w=1200&auto=format&fit=crop",
        popular: false
    },
    {
        id: 14,
        nombre: "Agua de Rio con Limon",
        descripcion: "Agua fresca saborizada naturalmente con limon.",
        categoria: "Bebidas",
        precio: 2200,
        imagen: "https://images.unsplash.com/photo-1513558161293-cdaf765ed2fd?q=80&w=1200&auto=format&fit=crop",
        popular: false
    }
];

let currentMenuItems = [];

document.addEventListener('DOMContentLoaded', () => {
    inicializarMenu();
});

// Función principal usando XMLHttpRequest (sin usar fetch)
function inicializarMenu() {
    const grid = document.getElementById('menu-container');
    const indicator = document.getElementById('api-status-indicator');

    mostrarCargando(grid);

    const xhr = new XMLHttpRequest();
    xhr.open('GET', BACKEND_URL, true);

    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            try {
                const data = JSON.parse(xhr.responseText);
                
                // Mapear los datos de inglés/español por compatibilidad
                currentMenuItems = data.map(item => normalizeItem(item));
                
                // Mostrar indicador de conexión exitosa
                actualizarIndicador(indicator, 'success', '[Conectado] Conectado al Pergamino del Rey (Backend Activo)');
            } catch (parseError) {
                console.error('Error parseando JSON del backend:', parseError);
                cargarMenuLocal(indicator);
            }
        } else {
            console.warn(`Error del servidor backend: Código ${xhr.status}`);
            cargarMenuLocal(indicator);
        }
        
        // Renderizar platos y configurar los botones de filtros
        renderizarPlatos(currentMenuItems, grid);
        configurarFiltros();
    };

    xhr.onerror = function () {
        console.warn('Error de red al conectar con el backend. Cargando datos locales.');
        cargarMenuLocal(indicator);
        
        // Renderizar platos y configurar los botones de filtros
        renderizarPlatos(currentMenuItems, grid);
        configurarFiltros();
    };

    xhr.send();
}

// Carga los banquetes locales en caso de error o backend inactivo
function cargarMenuLocal(indicator) {
    currentMenuItems = LOCAL_MENU;
    actualizarIndicador(indicator, 'warning', '[Conexión Local] Conexión con el Reino inestable (Usando registros locales de la taberna)');
    mostrarToast('Conexión con el backend fallida. Cargando banquetes locales.');
}

// Normaliza las propiedades de los platos (admite español e inglés)
function normalizeItem(item) {
    return {
        id: item.id || Math.random(),
        nombre: item.nombre || item.name || "Banquete sin nombre",
        descripcion: item.descripcion || item.description || "Un misterioso platillo del reino.",
        categoria: item.categoria || item.category || "Plato Principal",
        precio: item.precio || item.price || 0,
        imagen: item.imagen || item.image || "https://images.unsplash.com/photo-1514933651103-005eec06c04b?q=80&w=1200",
        popular: item.popular !== undefined ? item.popular : (item.isPopular || false)
    };
}

// Muestra el spinner de cargando
function mostrarCargando(container) {
    container.innerHTML = `
        <div class="loader-container" style="grid-column: 1 / -1;">
            <div class="loader"></div>
            <p>Preparando los banquetes y enfriando el hidromiel...</p>
        </div>
    `;
}

// Actualiza el banner superior de estado de API
function actualizarIndicador(element, status, message) {
    if (!element) return;
    element.className = `api-indicator ${status}`;
    element.innerHTML = `
        <span class="indicator-dot"></span>
        <span>${message}</span>
    `;
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

// Filtra las categorías normalizadas
function normalizeCategory(category) {
    return category.toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/\s+/g, '-');
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

// Notificación de Toast
function mostrarToast(mensaje) {
    let toast = document.getElementById('offline-toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'offline-toast';
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    toast.textContent = mensaje;
    // Forzar reflow
    toast.offsetHeight;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}
