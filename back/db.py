import pymysql
import os

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'root'),
        password=os.environ.get('DB_PASSWORD', ''),
        database=os.environ.get('DB_NAME', 'restaurante_db'),
        cursorclass=pymysql.cursors.DictCursor
    )

"""
def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',                      # Cambiado 'lara' por 'root'
        password='',                      # Dejado completamente vacío (sin el '1234')
        database='restaurante_db',        # Cambiado al nombre que pusimos en Workbench
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
"""
""" ------- Código anterior para referencia, no eliminar -------
def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='lara',
        password='1234',       
        database='restaurante_medieval',
        cursorclass=pymysql.cursors.DictCursor 
    )
    return connection
    """