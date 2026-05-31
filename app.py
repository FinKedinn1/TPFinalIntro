from flask import Flask, render_template, redirect, url_for, request 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/menu")
def menu():
    return render_template("Menu.html")

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
    app.run("127.0.0.1", port=5000, debug=True)