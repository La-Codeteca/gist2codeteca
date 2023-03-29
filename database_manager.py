import sqlite3

FILE_DATABASE_NAME = "procesed_gist.db"

def create_table():
    try:
        conexion=sqlite3.connect(FILE_DATABASE_NAME)
        conexion.execute("""create table if not exists gists (
                                codigo integer primary key AUTOINCREMENT,
                                id text,
                                process bool DEFAULT true,
                                create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                            )""")
        conexion.close()
    except sqlite3.OperationalError:
        print("La tabla articulos ya existe")  


def insert_data(data):
    print(f"Insertando: {data}")
    conexion=sqlite3.connect(FILE_DATABASE_NAME)
    conexion.execute("insert into gists(id) values (?)", (data, ))
    conexion.commit()
    conexion.close()

def get_all_data():
    id = []
    try:
        conexion=sqlite3.connect(FILE_DATABASE_NAME)
        query=conexion.execute("select id from gists")
        data=query.fetchall()      
        for fila in data:
            id.append(fila[0])
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conexion.close()
        return id

def get_data(id):
    conexion=sqlite3.connect(FILE_DATABASE_NAME)
    cursor=conexion.execute("select * from gists where id=?", (id, ))
    fila=cursor.fetchone()
    conexion.close()
    return fila

def exist_gist(id):
    conexion=sqlite3.connect(FILE_DATABASE_NAME)
    cursor=conexion.execute("select * from gists where id=?", (id, ))
    fila=cursor.fetchone()
    conexion.close()
    if fila!=None:
        return True
    else:
        return False
    
