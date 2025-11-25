
from db_connection import create_connection, close_connection

def ejecutar_script_sql(conn, ruta):
    cursor = conn.cursor()

    # Leer el archivo SQL
    with open(ruta, "r") as f:
        sql_script = f.read()

    #añade ; al final de cada sentencia, para separarlas correctamente
    statements = sql_script.split(";")

    # Ejecutar cada sentencia SQL
    for stmt in statements:
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt)

    conn.commit()
    cursor.close()

def insert_libro(conn, titulo, autor, disponible):
    query = """
    INSERT INTO libros (titulo, autor, disponible)
    VALUES (%s, %s, %s);
    """
    cursor = conn.cursor()
    cursor.execute(query, (titulo, autor, disponible))

    conn.commit()
    cursor.close()


def get_libros(conn):
    query = "SELECT id, titulo, autor, disponible, created_at FROM libros;"

    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    print("\nLibros registrados:")
    for r in rows:
        print(f"ID: {r[0]}, Título: {r[1]}, Autor: {r[2]}, Disponible: {r[3]}, Fecha: {r[4]}")

    cursor.close()


def insert_usuario(conn, nombre):
    query = """
    INSERT INTO usuarios (nombre)
    VALUES (%s);
    """
    cursor = conn.cursor()
    cursor.execute(query, (nombre,))

    conn.commit()
    cursor.close()


def get_usuarios(conn):
    query = "SELECT id, nombre, created_at FROM usuarios;"

    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    print("\nUsuarios registrados:")
    for r in rows:
        print(f"ID: {r[0]}, Nombre: {r[1]}, Fecha: {r[2]}")

    cursor.close()

def main():
    conn = create_connection()

    if conn:

        ejecutar_script_sql(conn, "src/bd.sql")

        
        insert_libro(conn, "Harry Potter", "J.K. Rowlien", 1)

        
        insert_usuario(conn, "Alan Hernandez")

        
        get_libros(conn)
        get_usuarios(conn)

        close_connection(conn)


if __name__ == "__main__":
    main()