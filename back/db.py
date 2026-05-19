import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='lara',
        password='1234',       
        database='restaurante_medieval',
        cursorclass=pymysql.cursors.DictCursor 
    )
    return connection