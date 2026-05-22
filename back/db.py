import pymysql

def get_db_connection():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',       
        database='restaurante_medieval',
        cursorclass=pymysql.cursors.DictCursor 
    )
    return connection