from flask import Blueprint, jsonify, request
from db import get_db_connection

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['GET'])
def mostrar_reservas():

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT reservas.*,usuarios.nombre FROM reservas JOIN usuarios ON reservas.id_usuario = usuarios.id_usuario"

    cursor.execute(query)

    reservas = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(reservas)


@reservas_bp.route('/reservas/<int:id>', methods=['GET'])
def mostrar_reserva_id(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT reservas.*,usuarios.nombre FROM reservas JOIN usuarios ON reservas.id_usuario = usuarios.id_usuario WHERE id_reserva = %s"

    cursor.execute(query, (id,))

    reserva = cursor.fetchone()

    cursor.close()
    conn.close()

    if reserva:
        return jsonify(reserva)

    return jsonify({
        "message": "Reserva no encontrada"
    }), 404


@reservas_bp.route('/reservas', methods=['POST'])
def crear_reserva():

    data = request.get_json()

    id_usuario = data.get('id_usuario')
    fecha_reserva = data.get('fecha_reserva')
    cant_personas = data.get('cant_personas')

    if not id_usuario or not fecha_reserva or not cant_personas:
        return jsonify({
            'message': 'Faltan datos para crear la reserva'
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO reservas (id_usuario, fecha_reserva, cant_personas)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (id_usuario, fecha_reserva, cant_personas))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        'message': 'Reserva creada exitosamente'
    }), 201


@reservas_bp.route('/reservas/<int:id>', methods=['PUT'])
def actualizar_reserva(id):

    data = request.get_json()

    id_usuario = data.get('id_usuario')
    fecha_reserva = data.get('fecha_reserva')
    cant_personas = data.get('cant_personas')

    if not id_usuario or not fecha_reserva or not cant_personas:
        return jsonify({
            'message': 'Faltan datos para actualizar la reserva'
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    UPDATE reservas
    SET id_usuario = %s, fecha_reserva = %s, cant_personas = %s
    WHERE id_reserva = %s
    """

    cursor.execute(query, (id_usuario, fecha_reserva, cant_personas, id))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        'message': 'Reserva actualizada exitosamente'
    }), 200



@reservas_bp.route('/reservas/<int:id>', methods=['DELETE'])
def eliminar_reserva(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = "DELETE FROM reservas WHERE id_reserva = %s"

    cursor.execute(query, (id,))

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        'message': 'Reserva eliminada exitosamente'
    }), 200