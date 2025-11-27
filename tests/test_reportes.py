import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))


import reportes
from reportes import Reportes


#mocks de conexión a BD
def fake_get_conn():
    return FakeConnection()


#clases fake para simular cursor y conexión
class FakeCursor:
    def __init__(self):
        self.executed = []
        self.lastrowid = 999
        self.one = ("2025-01-01 12:00:00", "REVISION")  # ejemplo de datos para fetchone

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchall(self):
        return [
            (1, 5, 7, "Motivo A", "2025-11-10 10:00:00", "REVISION"),
            (2, 6, 8, "Motivo B", "2025-11-11 10:00:00", "REVISION")
        ]

    def fetchone(self):
        return self.one

    def close(self):
        pass


class FakeConnection:
    def __init__(self):
        self.cursor_obj = FakeCursor()

    def cursor(self, dictionary=False):
        return self.cursor_obj

    def commit(self):
        pass

    def close(self):
        pass


#test
def test_crear_reporte(monkeypatch):
    #sustituir get_conn con mock
    monkeypatch.setattr(reportes, "get_conn", fake_get_conn)

    nuevo = Reportes.crear_reporte(5, 2, "Algo pasó")

    assert nuevo.id == 999
    assert nuevo.obra_id == 5
    assert nuevo.autor_id == 2
    assert nuevo.motivo == "Algo pasó"


def test_obtener_reportes_pendientes(monkeypatch):
    monkeypatch.setattr(reportes, "get_conn", fake_get_conn)

    lista = Reportes.obtener_reportes_pendientes()

    assert len(lista) == 2
    assert lista[0].motivo == "Motivo A"
    assert lista[1].estado == "REVISION"


def test_resolver_reporte(monkeypatch):
    conn = fake_get_conn()
    monkeypatch.setattr(reportes, "get_conn", lambda: conn)

    Reportes.resolver_reporte(10)

    # Validamos que se ejecutó el update
    executed = conn.cursor_obj.executed[-1]
    query, params = executed

    assert "UPDATE reportes SET estado = 'RESUELTO'" in query
    assert params == (10,)
