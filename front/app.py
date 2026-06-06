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

        puntaje_estrellas = request.form.get("puntaje_estrellas", 0)

        data = {
            "id_reserva": 1,  # obtener de la reserva del usuario
            "id_plato": 1,    # obtener del plato seleccionado
            "comentario": comentario,
            "puntaje_estrellas": puntaje_estrellas
        }

        requests.post(f"{API_BACKEND}/reseñas", json=data)

        return redirect(url_for("reseñas"))

    response = requests.get(f"{API_BACKEND}/reseñas")
    reseñas = response.json()

    return render_template("reseñas.html", reseñas=reseñas)


@app.route("/admin")
def admin():
    return render_template("admin/dashboard.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        datos_admin = {
            "email": request.form["email"],
            "password": request.form["password"]
        }
        respuesta = requests.post(f"{API_BACKEND}/login", json=datos_admin)        
        if respuesta.status_code == 200:
            return redirect(url_for("admin"))
    return render_template('admin/login.html')


@app.route("/admin/registro", methods=["GET", "POST"])
def admin_registro():
    if request.method == "POST":
        datos_registro = {
            "nombre": request.form.get("nombre"),
            "email": request.form.get("email"),
            "password": request.form.get("password")
        }
        respuesta = requests.post(f"{API_BACKEND}/usuarios", json=datos_registro)
        if respuesta.status_code == 201:
            return redirect(url_for("admin_login"))
    return render_template("admin/registro.html")


@app.route("/admin/menu", methods=["GET", "POST"])
def admin_menu():
    if request.method == "POST":
        datos_plato = {
            "nombre": request.form.get("nombre"),
            "precio": request.form.get("precio")
        }

        respuesta = requests.post(f"{API_BACKEND}/admin/menu", json=datos_plato)
        
        if respuesta.status_code == 201:
            return redirect(url_for("admin_menu"))

        return "Error al agregar plato", 500

    respuesta = requests.get(f"{API_BACKEND}/carta")
    lista_platos = respuesta.json()
    return render_template("admin/menu.html", platos=lista_platos)

@app.route("/admin/reservas")
def admin_reservas():
    respuesta = requests.get(f"{API_BACKEND}/reservas")
    lista_reservas = respuesta.json()
    return render_template("admin/reservas.html", reservas=lista_reservas)


@app.route("/admin/reseñas")
def admin_reseñas():
    respuesta = requests.get(f"{API_BACKEND}/reseñas")

    lista_reseñas = respuesta.json()
    return render_template("admin/reseñas.html", reseñas=lista_reseñas)

if __name__ == "__main__":
    app.run("127.0.0.1", port=5001, debug=True)
