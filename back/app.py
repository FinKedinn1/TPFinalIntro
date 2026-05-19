from flask import Flask
from flask_cors import CORS

from routes.menu import menu_bp
from routes.registro_usuarios import registro_usuarios_bp
from routes.reservas import reservas_bp
from routes.reseñas import reseñas_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(menu_bp)
app.register_blueprint(registro_usuarios_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(reseñas_bp)

if __name__ == '__main__':
    app.run(debug=True)