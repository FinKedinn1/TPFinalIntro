from flask import Flask, render_template

app = Flask(__name__)

@app.route('/menu')
def obtener_carta():
    return render_template("Menu.html")

@app.route('/index')
def index():
    return render_template("index.html")



if __name__ ==  '__main__':
    app.run("127.0.0.1", port="5000", debug=True)
    