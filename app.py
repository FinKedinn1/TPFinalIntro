from flask import Flask
from routes.menu import menu_bp
app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)