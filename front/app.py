from flask import Flask, render_template, redirect, url_for, request
import requests

API_BACKEND = "http://127.0.0.1:5000"
app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    responce = requests.get(f'{API_BACKEND}/carta')
    platos = responce.json()
    return render_template("Menu.html", platos=platos)

@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        email = request.form["email"]
        nombre_usuario = request.form["nombre_usuario"]
        contraseña = request.form["contraseña"]
        return redirect(url_for('login'))
    return render_template("registro.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        contraseña = request.form["contraseña"]
        return redirect(url_for('inicio'))
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

    return render_template("reservas.html")

@app.route("/reseñas", methods=["GET", "POST"])
def reseñas():
    if request.method == "POST":
        comentario = request.form["comentario"]
        return redirect(url_for('reseñas'))
    return render_template("reseñas.html")

if __name__ == "__main__":
    app.run("127.0.0.1", port=5001, debug=True)