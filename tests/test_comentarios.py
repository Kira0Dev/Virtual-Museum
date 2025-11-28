import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import comentarios
from comentarios import Comentarios as ComentarioClass


class FakeCursor:
    def __init__(self):
        self.executed = []
        self.lastrowid = 123
        #simula resultado de INSERT: id=123, fecha="2025-01-01 12:00:00"
        self.one = (123, "2025-01-01 12:00:00")

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchone(self):
        return self.one

    def close(self):
        pass

class FakeConnection:
    def __init__(self):
        self.cursor_obj = FakeCursor()

    def cursor(self):
        return self.cursor_obj

    def commit(self):
        pass

    def close(self):
        pass


def fake_get_conn():
    return FakeConnection()


def test_crear_comentario(monkeypatch):
    monkeypatch.setattr(comentarios, "get_conn", fake_get_conn)

    nuevo = ComentarioClass.crear_comentario(obra_id=10, autor_id=3, texto="Muy buena obra")

    #validaciones
    assert nuevo.id == 123
    assert nuevo.obra_id == 10
    assert nuevo.autor_id == 3
    assert nuevo.texto == "Muy buena obra"
    assert nuevo.fecha == "2025-01-01 12:00:00"


def test_eliminar_comentario_por_id(monkeypatch):
    conn = fake_get_conn()
    monkeypatch.setattr(comentarios, "get_conn", lambda: conn)

    ComentarioClass.eliminar_comentario_por_id(50)

    #asegura que se ejecutó el DELETE
    executed = conn.cursor_obj.executed[-1]
    query, params = executed

    assert "DELETE FROM comentarios WHERE id = %s" in query
    assert params == (50,)
