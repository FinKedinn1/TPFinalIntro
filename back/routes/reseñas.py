from flask import  Blueprint, jsonify, request
from db import get_db_connection

reseñas_bp = Blueprint("reseñas",__name__)

@reseñas_bp.route("/reseñas", methods =["GET"])
def mostrar_reseñas():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM reseñas"

    cursor.execute(query)
    reseñas = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(reseñas)

@reseñas_bp.route("/reseñas", methods =["POST"])
def crear_reseña():
    data = request.json

    id_reserva = data.get("id_reserva")
    comentario = data.get("comentario")
    puntaje = data.get("puntaje")

    obligatorio = ["id_reserva", "comentario", "puntaje"]

    for campo in obligatorio:
        if campo not in data:
            return jsonify({"Error": f"Falta {campo}"}), 400
        
    if puntaje < 1 or puntaje > 5:
        return {"Error": "Puntaje invàlido"}, 400

    connection = get_db_connection()
    cursor = connection.cursor()
   
    query = "SELECT * FROM reservas WHERE id_reserva = %s"
    cursor.execute (query, (id_reserva,))
    reserva = cursor.fetchone()

    if not reserva:
        cursor.close()
        connection.close()
        return{"Error": "La reserva no existe"}, 404
    
    sql = "INSERT INTO reseñas (id_reserva, comentario, puntaje) VALUES (%s, %s, %s)"

    cursor.execute(sql, (id_reserva,comentario,puntaje))

    connection.commit()
    cursor.close()
    connection.close()

    return {"Mensaje": "Reseña creada con exito"}, 201

@reseñas_bp.route("/reseñas/<int:id>", methods =["DELETE"])
def eliminar_reseña_id(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "DELETE FROM reseñas WHERE id_reseña = %s"

    cursor.execute(query, (id,))

    connection.commit()
    cursor.close()
    connection.close()

    
    return {"Mensaje": "Reseña eliminada con exito"}, 200  