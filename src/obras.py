from db_connection import get_conn

class Obras:
    def __init__(self, id, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags=[], estado_publicacion= "PENDIENTE"):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.autor_id = autor_id
        self.archivo_url = archivo_url
        self.miniatura_url = miniatura_url
        self.tags = tags
        self.estado_publicacion = estado_publicacion

    @classmethod
    def crear_obra(cls, titulo, descripcion, autor_id, archivo_url=None, miniatura_url=None, tags=[], estado_publicacion="PENDIENTE"):
        conn = get_conn()
        try:
            cur = conn.cursor()
            tags_str = ','.join(tags) if tags else None
            cur.execute(
                "INSERT INTO obras (titulo, descripcion, autor_id, archivo_url, miniatura_url, tags, estado_publicacion) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id",
                (titulo, descripcion, autor_id, archivo_url, miniatura_url, tags_str, estado_publicacion)
            )
            obra_id = cur.fetchone()[0]
            conn.commit()
            return cls(obra_id, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags, estado_publicacion)
        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_obra_por_id(cls, obra_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags, estado_publicacion FROM obras WHERE id = %s", (obra_id,))
            row = cur.fetchone()
            if row:
                tags = row[6].split(',') if row[6] else []
                return cls(row[0], row[1], row[2], row[3], row[4], row[5], tags, row[7])
            return None
        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_obras_por_autor(cls, autor_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags, estado_publicacion FROM obras WHERE autor_id = %s", (autor_id,))
            rows = cur.fetchall()
            obras = []
            for row in rows:
                tags = row[6].split(',') if row[6] else []
                obras.append(cls(row[0], row[1], row[2], row[3], row[4], row[5], tags, row[7]))
            return obras
        finally:    
            cur.close()
            conn.close()

    @classmethod
    def obtener_obra_por_titulo(cls, titulo):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags, estado_publicacion FROM obras WHERE titulo = %s", (titulo,))
            row = cur.fetchone()
            if row:
                tags = row[6].split(',') if row[6] else []
                return cls(row[0], row[1], row[2], row[3], row[4], row[5], tags, row[7])
            return None
        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_obras(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags, estado_publicacion FROM obras")
            rows = cur.fetchall()
            obras = []
            for row in rows:
                tags = row[6].split(',') if row[6] else []
                obras.append(cls(row[0], row[1], row[2], row[3], row[4], row[5], tags, row[7]))
            return obras
        finally:
            cur.close()
            conn.close()

    @classmethod
    def eliminar_obra_por_id(cls, obra_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM obras WHERE id = %s", (obra_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
            conn.close()

    @classmethod
    def actualizar_estado_publicacion(cls, obra_id, nuevo_estado):
        if nuevo_estado == "PENDIENTE" or nuevo_estado == "PUBLICADO" or nuevo_estado == "RECHAZADA":
            conn = get_conn()
            try:
                cur = conn.cursor()
                cur.execute("UPDATE obras SET estado_publicacion = %s WHERE id = %s", (nuevo_estado, obra_id))
                conn.commit()
                return cur.rowcount > 0
            finally:
                cur.close()
                conn.close()
        else:
            raise ValueError("Estado de publicación inválido. Debe ser 'PENDIENTE', 'PUBLICADO' o 'RECHAZADA'.")
        
    


        



    