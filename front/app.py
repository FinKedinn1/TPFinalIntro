
from flask import Flask, render_template, redirect, url_for, request, session
import requests



API_BACKEND = "http://127.0.0.1:5000"
app = Flask(__name__)
app.secret_key = "clave_secreta"


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    responce = requests.get(f'{API_BACKEND}/carta')
    platos = responce.json()
    response_populares = requests.get(f'{API_BACKEND}/menu/populares')
    platos_populares = response_populares.json()
    
    ids_platos_populares = [plato["id_plato"] for plato in platos_populares]
    return render_template("Menu.html", platos=platos, ids_platos_populares=ids_platos_populares)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        datos = {
                "nombre": request.form["nombre"],
                "email": request.form["email"],
                "password": request.form["password"]
            }
        respuesta = requests.post(f"{API_BACKEND}/usuarios",json=datos)
        if respuesta.status_code == 201:
                return redirect(url_for("login"))
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        datos = {
            "email": request.form["email"],
            "password": request.form["password"]
        }

        respuesta = requests.post(f"{API_BACKEND}/login", json=datos)

        if respuesta.status_code == 200:
            usuario = respuesta.json()["usuario"]

            session["usuario"] = usuario  

            return render_template("login_hecho.html", usuario=usuario)

        return render_template(
            "login.html",
            error="Email o contraseña incorrectos. Si no tienes cuenta, debes registrarte."
        )

    return render_template("login.html")

@app.route("/reservaciones", methods=["GET", "POST"])
def reservaciones():
    if request.method == "POST":
        fecha_reserva = request.form["fecha_reserva"]
        turno = request.form["turno"]
        cant_personas = int(request.form["cant_personas"])

        datos = {
            "id_usuario": 1,
            "fecha_reserva": fecha_reserva,
            "turno": turno,
            "cant_personas": cant_personas
        }

        respuesta = requests.post(f"{API_BACKEND}/reservas",json=datos)

        if respuesta.status_code == 201:
            return redirect(url_for("reservaciones"))

    response = requests.get(f"{API_BACKEND}/reservas")
    reservas = response.json()

    return render_template("reservas.html", reservas=reservas)

@app.route("/reseñas", methods=["GET", "POST"])
def reseñas():

    response = requests.get(f"{API_BACKEND}/reseñas")
    reseñas = response.json()

    if "usuario" not in session:
        return render_template(
            "login.html",
            reseñas=reseñas,
            error="Debes iniciar sesión para dejar una reseña."
        )

    if request.method == "POST":

        comentario = request.form["comentario"]
        puntaje_estrellas = request.form.get("puntaje_estrellas")

        if not puntaje_estrellas:
            return render_template(
                "reseñas.html",
                reseñas=reseñas,
                error="Debes seleccionar una cantidad de estrellas."
            )

        data = {
            "id_reserva": 1,
            "id_plato": 1,
            "comentario": comentario,
            "puntaje_estrellas": int(puntaje_estrellas)
        }

        respuesta = requests.post(f"{API_BACKEND}/reseñas", json=data)

        if respuesta.status_code != 201:
            return render_template(
                "reservas.html",
                reseñas=reseñas,
                error="Debes reservar para poder dejar una reseña."
            )

        return redirect(url_for("reseñas"))

    return render_template("reseñas.html", reseñas=reseñas)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run("127.0.0.1", port=5001, debug=True)