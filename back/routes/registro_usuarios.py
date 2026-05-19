from flask import  Blueprint, jsonify, request
from db import get_db_connection

registro_usuarios_bp = Blueprint("registro_usuarios",__name__)


@registro_usuarios_bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT id, nombre, email, rol, fecha_creacion
    FROM usuarios
    """

    cursor.execute(query)
    usuarios = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(usuarios)

@registro_usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT id, nombre, email, rol, fecha_creacion
    FROM usuarios
    WHERE id = %s
    """

    cursor.execute(query, (id,))
    usuario = cursor.fetchone()

    cursor.close()
    connection.close()

    return jsonify(usuario)

@registro_usuarios_bp.route('/usuarios', methods=['POST'])
def crear_usuario():
    data = request.get_json()
    nombre = data['nombre']
    email = data['email']
    password = data['password']

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO usuarios (nombre, email, password)
    VALUES (%s, %s, %s)
    """

    cursor.execute(query, (nombre, email, password))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "mensaje": "Usuario creado correctamente"
    })

@registro_usuarios_bp.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):

    data = request.get_json()
    nombre = data['nombre']
    email = data['email']
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE usuarios
    SET nombre = %s, email = %s
    WHERE id = %s
    """

    cursor.execute(query, (nombre, email, id))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "mensaje": "Usuario actualizado"
    })

@registro_usuarios_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = "DELETE FROM usuarios WHERE id = %s"

    cursor.execute(query, (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "mensaje": "Usuario eliminado"
    })
