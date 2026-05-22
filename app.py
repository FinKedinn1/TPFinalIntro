from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/menu')
def menu():
    return render_template("Menu.html")

@app.route('/historia')
def historia():
    return render_template("Historia.html")

@app.route('/contacto')
def contacto():
    return render_template("Contacto.html")

@app.route('/rankin')
def rankin():
    return render_template("Rankin.html")

if __name__ == '__main__':
    app.run("127.0.0.1", port="5000", debug=True)