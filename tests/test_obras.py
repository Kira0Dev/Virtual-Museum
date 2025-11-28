import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import obras
from obras import Obras as ObrasClass

class FakeCursor:
    def __init__(self):
        self.executed = []
        self.lastrowid = 777
        self.rowcount = 1
        self._dictionary_mode = False
        self._fetchone_data = None
        self._fetchall_data = None

    #soporta dictionary=True
    def set_dictionary_mode(self, value):
        self._dictionary_mode = value

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchone(self):
        return self._fetchone_data

    def fetchall(self):
        return self._fetchall_data

    def close(self):
        pass


class FakeConnection:
    def __init__(self):
        self.cursor_obj = FakeCursor()

    def cursor(self, dictionary=False):
        self.cursor_obj.set_dictionary_mode(dictionary)
        return self.cursor_obj

    def commit(self):
        pass

    def close(self):
        pass


def fake_get_conn():
    return FakeConnection()


def test_crear_obra(monkeypatch):
    conn = fake_get_conn()
    conn.cursor_obj._fetchone_data = (777,)

    monkeypatch.setattr(obras, "get_conn", lambda: conn)

    nueva = ObrasClass.crear_obra(
        "Título X", "Desc X", 5, "archivo.jpg", "mini.jpg", ["tag1", "tag2"], "PENDIENTE"
    )

    assert nueva.id == 777
    assert nueva.titulo == "Título X"
    assert nueva.descripcion == "Desc X"
    assert nueva.autor_id == 5
    assert nueva.tags == ["tag1", "tag2"]
    assert nueva.estado_publicacion == "PENDIENTE"


def test_obtener_obra_por_id(monkeypatch):
    conn = fake_get_conn()
    conn.cursor_obj._fetchone_data = {
        "id": 10,
        "titulo": "Obra Test",
        "descripcion": "Desc",
        "autor_id": 20,
        "archivo_url": "archivo.png",
        "miniatura_url": "mini.png",
        "tags": json.dumps(["fantasia", "arte"]),
        "estado_publicacion": "PUBLICADO",
        "fecha_subida": None,
        "contador_likes": 14
    }

    monkeypatch.setattr(obras, "get_conn", lambda: conn)

    obra = ObrasClass.obtener_obra_por_id(10)

    assert obra.id == 10
    assert obra.autor_id == 20
    assert obra.tags == ["fantasia", "arte"]
    assert obra.estado_publicacion == "PUBLICADO"


def test_obtener_obras_por_autor(monkeypatch):
    conn = fake_get_conn()
    conn.cursor_obj._fetchall_data = [
        {
            "id": 1,
            "titulo": "Obra1",
            "descripcion": "Desc1",
            "autor_id": 55,
            "archivo_url": "a1.png",
            "miniatura_url": "m1.png",
            "tags": json.dumps(["tagA"]),
            "estado_publicacion": "PENDIENTE",
            "fecha_subida": None,
            "contador_likes": 0
        },
        {
            "id": 2,
            "titulo": "Obra2",
            "descripcion": "Desc2",
            "autor_id": 55,
            "archivo_url": "a2.png",
            "miniatura_url": "m2.png",
            "tags": json.dumps(["tagB", "tagC"]),
            "estado_publicacion": "PUBLICADO",
            "fecha_subida": None,
            "contador_likes": 5
        }
    ]

    monkeypatch.setattr(obras, "get_conn", lambda: conn)

    obras_lista = ObrasClass.obtener_obras_por_autor(55)

    assert len(obras_lista) == 2
    assert obras_lista[0].tags == ["tagA"]
    assert obras_lista[1].tags == ["tagB", "tagC"]


def test_listar_obras(monkeypatch):
    conn = fake_get_conn()

    conn.cursor_obj._fetchall_data = [
        (1, "T1", "D1", 11, "a1.png", "m1.png", "tag1,tag2", "PENDIENTE"),
        (2, "T2", "D2", 22, "a2.png", "m2.png", "", "PUBLICADO"),
    ]

    monkeypatch.setattr(obras, "get_conn", lambda: conn)

    obras_lista = ObrasClass.listar_obras()

    assert len(obras_lista) == 2
    assert obras_lista[0].tags == ["tag1", "tag2"]
    assert obras_lista[1].tags == []


def test_eliminar_obra_por_id(monkeypatch):
    conn = fake_get_conn()
    conn.cursor_obj.rowcount = 1

    monkeypatch.setattr(obras, "get_conn", lambda: conn)

    resultado = ObrasClass.eliminar_obra_por_id(99)
    query, params = conn.cursor_obj.executed[-1]

    assert "DELETE FROM obras WHERE id = %s" in query
    assert params == (99,)
    assert resultado is True


def test_actualizar_estado_publicacion(monkeypatch):
    conn = fake_get_conn()

    monkeypatch.setattr(obras, "get_conn", lambda: conn)

    ok = ObrasClass.actualizar_estado_publicacion(5, "PUBLICADO")

    query, params = conn.cursor_obj.executed[-1]

    assert "UPDATE obras SET estado_publicacion = %s" in query
    assert params == ("PUBLICADO", 5)
    assert ok is True


def test_actualizar_estado_publicacion_invalido():
    try:
        ObrasClass.actualizar_estado_publicacion(5, "XXX")
        assert False, "Debe lanzar ValueError"
    except ValueError:
        assert True
