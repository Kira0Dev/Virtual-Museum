#Comentarios.py
from db_connection import get_conn

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
                "INSERT INTO comentarios (obra_id, autor_id, texto) VALUES (%s, %s, %s) RETURNING id, fecha",
                (obra_id, autor_id, texto)
            )
            resultado = cur.fetchone()
            conn.commit()
            return cls(resultado[0], obra_id, autor_id, texto, resultado[1])
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
        finally:
            cur.close()
            conn.close()