from flask import Blueprint, request, jsonify
from db import get_db_connection

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route("/admin/registro", methods=["POST"])
def api_admin_registrar():
    datos = request.json
    nombre = datos.get("nombre")
    email = datos.get("email")
    password = datos.get("password")

    if not nombre or not email or not password:
        return jsonify({"mensaje": "error de datos"}), 400
    
    return jsonify({"mensaje": "registro correcto"}), 201

@admin_bp.route("/admin/menu", methods=["POST"])
def admin_menu():
    datos = request.json
    nombre = datos.get("nombre")
    precio = datos.get("precio")

    if not nombre or not precio:
        return jsonify({"mensaje": "faltan datos"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    query = "INSERT INTO carta (nombre_plato, precio) VALUES (%s, %s)"

    cursor.execute(query, (nombre, precio))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"mensaje": "plato agregado correctamente"}), 201

@admin_bp.route("/admin/menu/<int:id_plato>", methods=["DELETE"])
def api_admin_menu_borrar(id_plato):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM carta WHERE id_plato = %s", (id_plato,))
    connection.commit()
    cursor.close()
    connection.close()
    
    return jsonify({"mensaje": "Plato borrado exitosamente"}), 200