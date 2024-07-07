import pymysql.cursors

def connect_to_db():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        db='juegoderol',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
