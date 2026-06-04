const estrellas = document.getElementsByClassName('estrella');

for (let i = 0; i < estrellas.length; i++) {
    estrellas[i].addEventListener('click', function() {

        for (let j = 0; j < estrellas.length; j++) {
            estrellas[j].classList.remove('activa');
        }

        for (let k = 0; k <= i; k++) {
            estrellas[k].classList.add('activa');
        }

        document.getElementById("puntaje_estrellas").value = i + 1;
    });
}

const formulario = document.querySelector("form");

formulario.addEventListener("submit", function(event) {

    const puntaje = document.getElementById("puntaje_estrellas").value;

    if (!puntaje) {
        event.preventDefault();
        alert("Debe seleccionar una cantidad de estrellas");
    }

});