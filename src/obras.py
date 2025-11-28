#obras.py
import logging
from db_connection import get_conn
import json

logging.basicConfig(level=logging.ERROR)

class Obras:
    def __init__(self, id, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags=[], estado_publicacion= "PENDIENTE", fecha_subida=None, contador_likes=0):
        self.id = id
        self.titulo = titulo
        self.descripcion = descripcion
        self.autor_id = autor_id
        self.archivo_url = archivo_url
        self.miniatura_url = miniatura_url
        self.tags = tags or []
        self.estado_publicacion = estado_publicacion
        self.fecha_subida = fecha_subida
        self.contador_likes = contador_likes

    @classmethod
    def crear_obra(cls, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags=None, estado_publicacion="PENDIENTE"):
        if tags is None:
            tags = []
        conn = get_conn()
        try:
            cur = conn.cursor()
            tags_json = json.dumps(tags)
            cur.execute(
                "INSERT INTO obras (titulo, descripcion, autor_id, archivo_url, miniatura_url, tags, estado_publicacion) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (titulo, descripcion, autor_id, archivo_url, miniatura_url, tags_json, estado_publicacion)
            )
            obra_id = cur.lastrowid
            conn.commit()
            return cls(obra_id, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags, estado_publicacion)
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al crear obra", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_obra_por_id(cls, obra_id):
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags, estado_publicacion FROM obras WHERE id = %s", (obra_id,))
            row = cur.fetchone()
            if row:
                tags = json.loads(row["tags"]) if row["tags"] else []
                return cls(
                    row["id"], row["titulo"], row["descripcion"], row["autor_id"],
                    row["archivo_url"], row["miniatura_url"], tags,
                    row["estado_publicacion"], row["fecha_subida"], row["contador_likes"]
                )
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al obtener obra por id", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()
            
    @classmethod
    def show_obra_visitante_por_id(cls, obra_id):
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, titulo, descripcion, autor_id, tags FROM obras WHERE id = %s", (obra_id,))
            #cur.execute("SELECT id, titulo, descripcion, autor_id, tags FROM obras WHERE id = %s AND estado_publicacion = 'PUBLICADO'", (obra_id,))
            row = cur.fetchone()
            if not row:
                return None
            row["tags"] = json.loads(row["tags"]) if row["tags"] else []
            return row

            
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al obtener obra por id para visitante", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_obras_por_autor(cls, autor_id):
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags, estado_publicacion FROM obras WHERE autor_id = %s", (autor_id,))
            rows = cur.fetchall()
            obras = []
            for row in rows:
                tags = json.loads(row["tags"]) if row["tags"] else []
                obras.append(cls(
                    row["id"], row["titulo"], row["descripcion"], row["autor_id"],
                    row["archivo_url"], row["miniatura_url"], tags,
                    row["estado_publicacion"]
                ))
            return obras
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al obtener obras por autor", exc_info=True)
            raise

        finally:    
            cur.close()
            conn.close()

    @classmethod
    def obtener_obra_por_titulo(cls, titulo):
        conn = get_conn()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, titulo, descripcion, autor_id, archivo_url, miniatura_url, tags, estado_publicacion FROM obras WHERE titulo = %s", (titulo,))
            row = cur.fetchone()

            if row is None:
                return None

            tags = json.loads(row["tags"]) if row["tags"] else []

            return cls(
                row["id"], row["titulo"], row["descripcion"], row["autor_id"],
                row["archivo_url"], row["miniatura_url"], tags, row["estado_publicacion"]
            )

        except Exception as e:
            print("Error:", e)
            raise

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
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al listar obras", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def show_obras_visitante(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT titulo, descripcion, autor_id FROM obras LIMIT 10")
            #cur.execute("SELECT titulo, descripcion, autor_id FROM obras LIMIT 10 WHERE estado_publicacion = 'PUBLICADO'")
            rows = cur.fetchall()
            obras = []
            for row in rows:
                obra = {
                    "titulo": row[0],
                    "descripcion": row[1],
                    "autor_id": row[2]
                }
                obras.append(obra)
            return obras
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al listar obras", exc_info=True)
            raise

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
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al eliminar obra", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def eliminar_obra_por_titulo(cls, titulo, autor_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT autor_id FROM obras WHERE titulo = %s", (titulo,))
            row = cur.fetchone()
            if not row or row[0] != autor_id:
                return False
            else:
                cur.execute("DELETE FROM obras WHERE titulo = %s AND autor_id = %s", (titulo, autor_id))
                conn.commit()
                return cur.rowcount > 0
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al eliminar obra por titulo", exc_info=True)
            raise

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
            
            except Exception as e:
                conn.rollback()
                logging.error(f"Error al actualizar estado de publicacion", exc_info=True)
                raise

            finally:
                cur.close()
                conn.close()
        else:
            raise ValueError("Estado de publicación inválido. Debe ser 'PENDIENTE', 'PUBLICADO' o 'RECHAZADA'.")
        
    def __str__(self):
        return f"Obra(id={self.id}, titulo='{self.titulo}', descripcion='{self.descripcion}', autor_id={self.autor_id}, archivo_url='{self.archivo_url}', miniatura_url='{self.miniatura_url}', tags={self.tags}, estado_publicacion='{self.estado_publicacion}', fecha_subida={self.fecha_subida}, contador_likes={self.contador_likes})"
        