const estrellas = document.getElementsByClassName('estrella');

for (let i = 0; i < estrellas.length; i++) {
    estrellas[i].addEventListener('click', function() {
        for (let j = 0; j < estrellas.length; j++) {
            estrellas[j].classList.remove('activa');
        }
        for (let k = 0; k <= i; k++) {
            estrellas[k].classList.add('activa');
        }
    });
}

document.getElementById("form-reseña").addEventListener("submit", async function(e) {
    e.preventDefault();

    const comentario = document.getElementById("comentario").value;

    const puntaje = document.getElementsByClassName("activa").length;

    const data = {
        id_reserva: 1,
        id_plato: 1,
        comentario: comentario,
        puntaje_estrellas: puntaje
    };

    const res = await fetch("http://127.0.0.1:5000/reseñas", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    const result = await res.json();
    alert(result.Mensaje || result.Error);

    document.getElementById("form-reseña").reset();

    cargarReseñas();
});


async function cargarReseñas() {
    const res = await fetch("http://127.0.0.1:5000/reseñas");
    const data = await res.json();

    const contenedor = document.getElementById("contenedor-reseñas");

    contenedor.innerHTML = "";

    data.forEach(r => {
        const div = document.createElement("div");

        div.innerHTML = `
            <p><strong>Comentario:</strong> ${r.comentario}</p>
            <p><strong>⭐</strong> ${r.puntaje_estrellas}</p>
            <hr>
        `;

        contenedor.appendChild(div);
    });
}

cargarReseñas();