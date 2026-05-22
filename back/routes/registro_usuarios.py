from flask import Blueprint, jsonify, request
from db import get_db_connection

registro_usuarios_bp = Blueprint("registro_usuarios", __name__)


@registro_usuarios_bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT id_usuario, nombre, email, fecha_creacion
    FROM usuarios
    """

    cursor.execute(query)
    usuarios = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(usuarios)


@registro_usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['GET'])
def obtener_usuario(id_usuario):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT id_usuario, nombre, email, fecha_creacion
    FROM usuarios
    WHERE id_usuario = %s
    """

    cursor.execute(query, (id_usuario,))
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


@registro_usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):

    data = request.get_json()

    nombre = data['nombre']
    email = data['email']

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    UPDATE usuarios
    SET nombre = %s, email = %s
    WHERE id_usuario = %s
    """

    cursor.execute(query, (nombre, email, id_usuario))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "mensaje": "Usuario actualizado"
    })


@registro_usuarios_bp.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):

    connection = get_db_connection()
    cursor = connection.cursor()

    query = "DELETE FROM usuarios WHERE id_usuario = %s"

    cursor.execute(query, (id_usuario,))
    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "mensaje": "Usuario eliminado"
    })

@registro_usuarios_bp.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data['email']
    password = data['password']

    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
    SELECT id_usuario, nombre, email
    FROM usuarios
    WHERE email = %s AND password = %s
    """

    cursor.execute(query, (email, password))
    usuario = cursor.fetchone()

    cursor.close()
    connection.close()

    if usuario:
        return jsonify({
            "mensaje": "Login exitoso",
            "usuario": usuario
        })

    return jsonify({
        "mensaje": "Email o contraseña incorrectos"
    }), 401