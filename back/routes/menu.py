from flask import  Blueprint, jsonify, request
from db import get_db_connection

menu_bp = Blueprint("menu",__name__)

@menu_bp.route("/menu", methods=["GET"])
def mostrar_menu():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM menu"

    cursor.execute(query)
    menu = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(menu)

@menu_bp.route("/menu/<int:id>", methods=["GET"])
def mostrar_plato(id):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM menu WHERE id_menu = %s"
    cursor.execute(query, (id,))
    plato = cursor.fetchone()
    cursor.close()
    connection.close()

    if plato:
        return jsonify(plato),200
    return jsonify({
        "error": "Plato no encontrado"
    }), 404

@menu_bp.route("/menu/populares", methods=["GET"])
def platos_populares():

    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM menu WHERE popular = TRUE"
    cursor.execute(query)
    resultado = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(resultado)

@menu_bp.route("/menu/categoria/<categoria>", methods=["GET"])
def categoria_plato(categoria):
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM menu WHERE categoria = %s"
    cursor.execute(query, (categoria,))
    resultado = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(resultado)

