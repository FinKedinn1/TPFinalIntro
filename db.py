import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='mi_usuario',
        password='mi_contraseña',       
        database='restaurante_medieval',
        cursorclass=pymysql.cursors.DictCursor 
    )
    return connection