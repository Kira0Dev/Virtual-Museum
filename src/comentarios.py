#Comentarios.py
import logging
from db_connection import get_conn

logging.basicConfig(level=logging.ERROR)

class Comentarios:
    def __init__(self,id, obra_id, autor_id, texto, fecha=None, estado='VISIBLE'):
        self.id = id
        self.obra_id = obra_id
        self.autor_id = autor_id
        self.texto = texto
        self.fecha = fecha
        self.estado = estado

    @classmethod
    def crear_comentario(cls, obra_id, autor_id, texto):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO comentarios (obra_id, autor_id, texto) VALUES (%s, %s, %s)",
                (obra_id, autor_id, texto)
            )
            comentario_id = cur.lastrowid 
            conn.commit()
            return cls(comentario_id, obra_id, autor_id, texto)
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al crear comentario", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def eliminar_comentario_por_id(cls, comentario_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM comentarios WHERE id = %s",
                (comentario_id,)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al eliminar comentario", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"Comentario(id={self.id}, obra_id={self.obra_id}, autor_id={self.autor_id}, texto='{self.texto}', fecha={self.fecha}, estado='{self.estado}')"