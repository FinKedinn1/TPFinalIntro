// Base de datos local de Héroes de la Taberna
const HEROES_DATABASE = [
    {
        rango: 1,
        nombre: "Sir Lancelot de Quilmes",
        reino: "Reino de Buenos Aires",
        titulo: "Vencedor del Chivito Gigante de Fuego",
        renombre: 9850,
        platoFavorito: "Hamburguesa del Rey"
    },
    {
        rango: 2,
        nombre: "Geralt de Banfield",
        reino: "Tierras del Viento (Sur)",
        titulo: "Exterminador de Plagas de la Bodega",
        renombre: 8900,
        platoFavorito: "Jabali al Ajillo"
    },
    {
        rango: 3,
        nombre: "Lagertha de Morón",
        reino: "Fiordos del Este",
        titulo: "Campeona Invicta de Fondo Blanco de Hidromiel",
        renombre: 8120,
        platoFavorito: "Hidromiel"
    },
    {
        rango: 4,
        nombre: "Legolas de La Plata",
        reino: "Reino del Norte (Bosque)",
        titulo: "Arquero Vegano y Catador de Pócimas",
        renombre: 7500,
        platoFavorito: "Pasteles de Carne de Soja"
    },
    {
        rango: 5,
        nombre: "Frodo de Avellaneda",
        reino: "Tierra Media (Oeste)",
        titulo: "Portador de la Tarta de Manzana Sagrada",
        renombre: 6950,
        platoFavorito: "Tarta del Guerrero"
    },
    {
        rango: 6,
        nombre: "Conan el del Abasto",
        reino: "Reino de Buenos Aires",
        titulo: "Devorador de Tres Cazuelas de Guiso Seguidas",
        renombre: 6200,
        platoFavorito: "Guiso de Pichon de Gorrion"
    },
    {
        rango: 7,
        nombre: "Aragorn de San Isidro",
        reino: "Reino del Norte (Tierras Altas)",
        titulo: "Montaraz del Buen Diente y la Espada Larga",
        renombre: 5800,
        platoFavorito: "Liebre al Escabeche"
    },
    {
        rango: 8,
        nombre: "Gimli el de Lanús",
        reino: "Montañas de Metal",
        titulo: "Tallador de Jarras y Comensal Veloz",
        renombre: 5400,
        platoFavorito: "Papas del Castillo"
    }
];

document.addEventListener('DOMContentLoaded', () => {
    const tbody = document.getElementById('ranking-tbody');
    const searchInput = document.getElementById('hero-search');

    // Inicializar renderizado
    renderizarRanking(HEROES_DATABASE, tbody);

    // Configurar buscador interactivo en tiempo real
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const query = searchInput.value.toLowerCase().trim();
            
            const filteredHeroes = HEROES_DATABASE.filter(heroe => {
                return heroe.nombre.toLowerCase().includes(query) || 
                       heroe.reino.toLowerCase().includes(query) ||
                       heroe.titulo.toLowerCase().includes(query) ||
                       heroe.platoFavorito.toLowerCase().includes(query);
            });

            renderizarRanking(filteredHeroes, tbody);
        });
    }
});

// Función de renderizado dinámico de filas
function renderizarRanking(heroes, container) {
    container.innerHTML = '';

    if (heroes.length === 0) {
        container.innerHTML = `
            <tr>
                <td colspan="6" style="text-align: center; font-style: italic; color: #7a5c2e; padding: 30px;">
                    Ningún guerrero de renombre coincide con tu pergamino de búsqueda...
                </td>
            </tr>
        `;
        return;
    }

    heroes.forEach(heroe => {
        const tr = document.createElement('tr');
        
        // Determinar estilo del Rango
        let badgeClass = 'rank-other';
        if (heroe.rango === 1) badgeClass = 'rank-1';
        else if (heroe.rango === 2) badgeClass = 'rank-2';
        else if (heroe.rango === 3) badgeClass = 'rank-3';

        // Formatear Puntos
        const formattedPoints = new Intl.NumberFormat('es-AR').format(heroe.renombre);

        tr.innerHTML = `
            <td style="text-align: center; vertical-align: middle;">
                <span class="rank-badge ${badgeClass}">${heroe.rango}</span>
            </td>
            <td><strong>${heroe.nombre}</strong></td>
            <td>${heroe.reino}</td>
            <td><span style="font-size: 0.95rem; color: #5c3e26; font-style: italic;">"${heroe.titulo}"</span></td>
            <td style="text-align: right; font-weight: bold; color: #4a2e1b;">${formattedPoints}</td>
            <td><span style="background: rgba(212, 160, 23, 0.15); border: 1px dashed #b89158; padding: 4px 8px; border-radius: 4px; font-size: 0.9rem;">${heroe.platoFavorito}</span></td>
        `;
        
        container.appendChild(tr);
    });
}
