from flask import Blueprint, jsonify, request
from db import get_db_connection

reservas_bp = Blueprint('reservas', __name__)

@reservas_bp.route('/reservas', methods=['GET'])
def mostrar_reservas():

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT reservas.*,usuarios.nombre FROM reservas 
    JOIN usuarios ON reservas.id_usuario = usuarios.id_usuario
    ORDER BY reservas.fecha_reserva, turno
    """

    cursor.execute(query)

    reservas = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(reservas)


@reservas_bp.route('/reservas/<int:id>', methods=['GET'])
def mostrar_reserva_id(id):

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """SELECT reservas.*,usuarios.nombre FROM reservas 
    JOIN usuarios ON reservas.id_usuario = usuarios.id_usuario 
    WHERE id_reserva = %s
    """

    cursor.execute(query, (id,))

    reserva = cursor.fetchone()

    cursor.close()
    conn.close()

    if reserva:
        return jsonify(reserva)

    return jsonify({
        "Mensaje": "Reserva no encontrada"
    }), 404

@reservas_bp.route('/reservas/disponibilidad', methods=['GET'])
def ver_disponibilidad():

    fecha = request.args.get("fecha")

    if not fecha:
        return jsonify({"Mensaje": "Se necesita la fecha"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        consulta = """
        SELECT turno, SUM(cant_personas)
        FROM reservas
        WHERE fecha_reserva = %s
        GROUP BY turno
        """

        cursor.execute(consulta, (fecha,))
        resultados = cursor.fetchall()
    
        capacidad_max = 60
        respuesta = []

        for turno in ["20-22", "22-00"]:
            ocupado = 0

            for resultado in resultados:
                if resultado[0] == turno:
                    ocupado = resultado[1] or 0

            respuesta.append({
                "turno": turno,
                "disponible": capacidad_max - ocupado
            })

        return jsonify(respuesta), 200

    except Exception:
        return jsonify({
            "Mensaje": "Error al buscar la disponibilidad"
        }), 500
    
    finally:
        cursor.close()
        conn.close()

   
@reservas_bp.route('/reservas', methods=['POST'])
def crear_reserva():

    data = request.get_json()

    id_usuario = data.get('id_usuario')
    fecha_reserva = data.get('fecha_reserva')
    cant_personas = data.get('cant_personas')
    turno = data.get('turno')

    if not id_usuario or not fecha_reserva or not cant_personas or not turno:
        return jsonify({
            "Mensaje": "Faltan datos para crear la reserva"
        }), 400
    
    if turno not in ["20-22", "22-00"]:
        return jsonify ({"Mensaje": "Turno invalido"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        check = """
        SELECT SUM(cant_personas) FROM reservas
        WHERE fecha_reserva = %s
        AND turno = %s
        """

        cursor.execute(check, (fecha_reserva, turno))
        resultado = cursor.fetchone()[0]

        capacidad_max = 60

        if (resultado or 0) + cant_personas > capacidad_max:
            return jsonify ({
                "Mensaje": "No hay disponibilidad para esta fecha"
            }), 400

        query = """
        INSERT INTO reservas (id_usuario, fecha_reserva, cant_personas, turno)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (id_usuario, fecha_reserva, cant_personas, turno))

        conn.commit()

        return jsonify({
            "Mensaje": "Reserva creada exitosamente"
        }), 201
    
    except Exception:
        conn.rollback()
        return jsonify({
            "Mensaje": "Error con la reserva"
        }), 500
    
    finally:
        cursor.close()
        conn.close()


@reservas_bp.route('/reservas/<int:id>', methods=['PUT'])
def actualizar_reserva(id):

    data = request.get_json()

    id_usuario = data.get('id_usuario')
    fecha_reserva = data.get('fecha_reserva')
    cant_personas = data.get('cant_personas')
    turno = data.get ('turno')

    if not id_usuario or not fecha_reserva or not cant_personas or not turno:
        return jsonify({
            "Mensaje": "Faltan datos para actualizar la reserva"
        }), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        #Valido la capacidad sin incluir la reserva actual
        check = """
        SELECT SUM(cant_personas) FROM reservas
        WHERE fecha_reserva = %s
        AND id_reserva != %s
        AND turno = %s
        """

        cursor.execute(check, (fecha_reserva, id, turno))
        resultado = cursor.fetchone()[0]

        capacidad_max = 60

        if (resultado or 0) + cant_personas > capacidad_max:
            return jsonify ({
                "Mensaje": "No hay disponibilidad para esta fecha"
            }), 400

        query = """
        UPDATE reservas
        SET id_usuario = %s, fecha_reserva = %s, cant_personas = %s, turno = %s
        WHERE id_reserva = %s
        """

        cursor.execute(query, (id_usuario, fecha_reserva, cant_personas, turno, id))

        conn.commit()

        return jsonify({
            "Mensaje": "Reserva actualizada exitosamente"
        }), 200
    
    except Exception:
        conn.rollback()
        return jsonify({
            "Mensaje": "Error con la reserva"
        }), 500

    finally:
        cursor.close()
        conn.close()

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
        "Mensaje": "Reserva eliminada exitosamente"
    }), 200