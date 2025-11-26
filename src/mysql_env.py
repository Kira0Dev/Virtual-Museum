from db_connection import create_connection, close_connection

def ejecutar_script_sql(conn, ruta):
    cursor = conn.cursor()

    #leer el archivo SQL
    with open(ruta, "r") as f:
        sql_script = f.read()

    #dividir el script con ;
    statements = sql_script.split(";")

    #leer y ejecutar cada sentencia
    for stmt in statements:
        stmt = stmt.strip()
        if stmt:
            cursor.execute(stmt)

    conn.commit()
    cursor.close()


#insertar usuarios de prueba
def insert_usuario(conn, nombre, email, password_hash, rol="VISITANTE"):
    query = """
    INSERT INTO usuarios (nombre, email, password_hash, rol)
    VALUES (%s, %s, %s, %s);
    """

    cursor = conn.cursor()
    cursor.execute(query, (nombre, email, password_hash, rol))
    conn.commit()
    cursor.close()


#consultar usuarios
def get_usuarios(conn):
    query = "SELECT id, nombre, email, rol, fecha_registro FROM usuarios;"

    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    print("\nUsuarios registrados:")
    for r in rows:
        print(f"ID: {r[0]}, Nombre: {r[1]}, Email: {r[2]}, Rol: {r[3]}, Fecha: {r[4]}")

    cursor.close()

#insertar obra de prueba
def insert_obra(conn, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags="[]"):
    query = """
    INSERT INTO obras (titulo, descripcion, autor_id, archivo_url, miniatura_url, tags)
    VALUES (%s, %s, %s, %s, %s, %s);
    """

    cursor = conn.cursor()
    cursor.execute(query, (titulo, descripcion, autor_id, archivo_url, miniatura_url, tags))
    conn.commit()
    cursor.close()


# consultar obras
def get_obras(conn):
    query = "SELECT id, titulo, autor_id, fecha_subida FROM obras;"

    cursor = conn.cursor()
    cursor.execute(query)

    rows = cursor.fetchall()
    print("\nObras registradas:")
    for r in rows:
        print(f"ID: {r[0]}, Título: {r[1]}, Autor: {r[2]}, Fecha: {r[3]}")

    cursor.close()


#main
def main():
    conn = create_connection()

    if conn:
        ejecutar_script_sql(conn, "src/bd.sql")

        #crear usuarios de prueba
        insert_usuario(conn, "Carlos Visitante", "visitante@test.com", "hash123", "VISITANTE")
        insert_usuario(conn, "Ana Artista", "artista@test.com", "hash123", "ARTISTA")
        insert_usuario(conn, "Luis Moderador", "mod@test.com", "hash123", "MODERADOR")

        #obtener el ID del artista recién creado para la obra
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", ("artista@test.com",))
        artista_id = cursor.fetchone()[0]
        cursor.close()

        #registrar una obra del artista
        insert_obra(
            conn,
            "Atardecer Digital",
            "Un atardecer sobre una hermosa computadora",
            artista_id,
            "ruta_pendiente",
            "ruta_pendiente",
            '["digital", "arte"]'
        )

        #mostrar resultados
        get_usuarios(conn)
        get_obras(conn)

        close_connection(conn)


if __name__ == "__main__":
    main()
