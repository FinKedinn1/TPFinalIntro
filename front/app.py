from flask import Flask, render_template, redirect, url_for, request
import requests

API_BACKEND = "http://127.0.0.1:5000"
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    responce = requests.get(f'{API_BACKEND}/carta')
    platos = responce.json()
    return render_template("Menu.html", platos=platos)

@app.route("/registro")
def registro():
    return render_template("registro.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/reservaciones")
def reservaciones():
    return render_template("reservas.html")

@app.route("/reseñas")
def reseñas():
    return render_template("reseñas.html")

if __name__ == "__main__":
    app.run("127.0.0.1", port=5001, debug=True)