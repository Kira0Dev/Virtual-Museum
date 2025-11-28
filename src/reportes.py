#reportes.py
from db_connection import get_conn

class Reportes:
    def __init__(self, id, obra_id, autor_id, motivo, fecha=None, estado='REVISION'):
        self.id = id
        self.obra_id = obra_id
        self.autor_id = autor_id
        self.motivo = motivo
        self.fecha = fecha
        self.estado = estado

    @classmethod
    def crear_reporte(cls, obra_id, autor_id, motivo):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO reportes (obra_id, autor_id, motivo) VALUES (%s, %s, %s)",
                (obra_id, autor_id, motivo)
            )
            conn.commit()
            reporte_id = cur.lastrowid
            cur.execute(
                "SELECT fecha, estado FROM reportes WHERE id = %s",
                (reporte_id,)
            )
            fila = cur.fetchone()
            return cls(reporte_id, obra_id, autor_id, motivo, fila[0], fila[1])
        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_reportes_pendientes(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, obra_id, autor_id, motivo, fecha, estado FROM reportes WHERE estado = 'REVISION'"
            )
            filas = cur.fetchall()
            reportes = [cls(*fila) for fila in filas]
            return reportes
        finally:
            cur.close()
            conn.close()

    @classmethod
    def resolver_reporte(cls, reporte_id):
        if reporte_id is None:
            return
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id FROM reportes WHERE id = %s",
                (reporte_id,)
            )
            if cur.fetchone() is None:
                return
            cur.execute(
                "UPDATE reportes SET estado = 'RESUELTO' WHERE id = %s",
                (reporte_id,)
            )
            conn.commit()
        finally:
            cur.close()
            conn.close()

    def __str__(self):
        return f"Reporte(id={self.id}, obra_id={self.obra_id}, autor_id={self.autor_id}, motivo='{self.motivo}', fecha={self.fecha}, estado='{self.estado}')"