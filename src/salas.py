#salas.py
import logging
from db_connection import get_conn

logging.basicConfig(level=logging.ERROR)

privacidad_options = ["PUBLICA", "PRIVADA"]

class Salas:
    def __init__(self, id, autor_id, nombre, descripcion, privacidad="PUBLICA", codigo_acceso=None):
        self.id = id
        self.autor_id = autor_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.privacidad = privacidad
        self.codigo_acceso = codigo_acceso

    @classmethod
    def crear_sala(cls, autor_id, nombre, descripcion, privacidad, codigo_acceso):
        if privacidad not in privacidad_options:
            raise ValueError("Privacidad inválida. Debe ser 'PUBLICA' o 'PRIVADA'.")
        
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO salas (autor_id, nombre, descripcion, privacidad, codigo_acceso) VALUES (%s, %s, %s, %s, %s)",
                (autor_id, nombre, descripcion, privacidad, codigo_acceso)
            )
            conn.commit()
            sala_id = cur.lastrowid
            return cls(sala_id, autor_id, nombre, descripcion, privacidad, codigo_acceso)
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al crear sala", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def eliminar_sala_por_id(cls, sala_id):
        if sala_id is None:
            return
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM salas WHERE id = %s",
                (sala_id,)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al eliminar sala", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_salas_publicas(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, autor_id, nombre, descripcion, privacidad, codigo_acceso FROM salas WHERE privacidad = 'PUBLICA'"
            )
            filas = cur.fetchall()
            salas = [cls(*fila) for fila in filas]
            return salas
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al listar salas publicas", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_sala_por_id(cls, sala_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, autor_id, nombre, descripcion, privacidad, codigo_acceso FROM salas WHERE id = %s",
                (sala_id,)
            )
            fila = cur.fetchone()
            if fila:
                return cls(*fila)
            return None
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al obtener sala por id", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def buscar_sala_por_nombre(cls, nombre):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, autor_id, nombre, descripcion, privacidad, codigo_acceso FROM salas WHERE nombre = %s",
                (nombre,)
            )

            filas = cur.fetchall()
            salas = [cls(*fila) for fila in filas]
            return salas
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al buscar sala por nombre", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def añadir_obra_a_sala(cls, sala_id, obra_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO salas_obras (sala_id, obra_id) VALUES (%s, %s)",
                (sala_id, obra_id)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al añadir obra a sala", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def show_obras_en_sala(cls, sala_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT obra_id FROM salas_obras WHERE sala_id = %s",
                (sala_id,)
            )
            rows = cur.fetchall() 
            obra_ids = [row[0] for row in rows]
            return obra_ids

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al buscar obras de sala", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()


    def __str__(self):
        return f"Sala(id={self.id}, autor_id={self.autor_id}, nombre='{self.nombre}', descripcion='{self.descripcion}', privacidad='{self.privacidad}', codigo_acceso='{self.codigo_acceso}')"