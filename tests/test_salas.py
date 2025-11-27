import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import salas
from salas import Salas


def fake_get_conn():
    return FakeConnection()


class FakeCursor:
    def __init__(self):
        self.executed = []
        self.lastrowid = 123 
        self.one = (
            1, 5, "Sala Uno", "Desc", "PUBLICA", None
        )  #datos para fetchone()

        #datos de ejemplo para fetchall
        self.many = [
            (1, 5, "Sala Uno", "Desc A", "PUBLICA", None),
            (2, 6, "Sala Dos", "Desc B", "PUBLICA", None)
        ]

    def execute(self, query, params=None):
        self.executed.append((query, params))

    def fetchall(self):
        return self.many

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


#test crear_sala
def test_crear_sala(monkeypatch):
    monkeypatch.setattr(salas, "get_conn", fake_get_conn)

    nueva = Salas.crear_sala(
        autor_id=5,
        nombre="Sala Test",
        descripcion="Una sala de prueba",
        privacidad="PUBLICA",
        codigo_acceso=None
    )

    assert nueva.id == 123
    assert nueva.autor_id == 5
    assert nueva.nombre == "Sala Test"
    assert nueva.privacidad == "PUBLICA"


#test crear_sala con privacidad inválida
def test_crear_sala_privacidad_invalida():
    try:
        Salas.crear_sala(1, "X", "Y", "SECRETA", None)
        assert False, "Debió lanzar ValueError"
    except ValueError:
        assert True


#test eliminar_sala
def test_eliminar_sala(monkeypatch):
    conn = fake_get_conn()
    monkeypatch.setattr(salas, "get_conn", lambda: conn)

    Salas.eliminar_sala_por_id(10)

    #verificar que ejecutó DELETE correctamente
    query, params = conn.cursor_obj.executed[-1]
    assert "DELETE FROM salas WHERE id" in query
    assert params == (10,)


#test listar_salas_publicas
def test_listar_salas_publicas(monkeypatch):
    monkeypatch.setattr(salas, "get_conn", fake_get_conn)

    lista = Salas.listar_salas_publicas()

    assert len(lista) == 2
    assert lista[0].nombre == "Sala Uno"
    assert lista[1].nombre == "Sala Dos"
    assert lista[0].privacidad == "PUBLICA"


#test obtener_sala_por_id
def test_obtener_sala_por_id(monkeypatch):
    monkeypatch.setattr(salas, "get_conn", fake_get_conn)

    sala = Salas.obtener_sala_por_id(1)

    assert sala is not None
    assert sala.id == 1
    assert sala.nombre == "Sala Uno"


#test buscar_sala_por_nombre
def test_buscar_sala_por_nombre(monkeypatch):
    monkeypatch.setattr(salas, "get_conn", fake_get_conn)

    resultados = Salas.buscar_sala_por_nombre("Sala Uno")

    assert len(resultados) == 2
    assert resultados[0].nombre == "Sala Uno"


#test añadir_obra_a_sala
def test_añadir_obra_a_sala(monkeypatch):
    conn = fake_get_conn()
    monkeypatch.setattr(salas, "get_conn", lambda: conn)

    Salas.añadir_obra_a_sala(3, 7)

    query, params = conn.cursor_obj.executed[-1]

    assert "INSERT INTO salas_obras" in query
    assert params == (3, 7)
