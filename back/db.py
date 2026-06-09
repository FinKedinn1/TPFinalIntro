import pymysql
import os
"""
def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        user=os.environ.get('DB_USER', 'lara'),
        password=os.environ.get('DB_PASSWORD', '1234'), 
        database=os.environ.get('DB_NAME', 'restaurante_db'),
        cursorclass=pymysql.cursors.DictCursor
    )
"""

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='lara',                      # Cambiado 'lara' por 'root'
        password='1234',                      # Dejado completamente vacío (sin el '1234')
        database='restaurante_medieval',        # Cambiado al nombre que pusimos en Workbench
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

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