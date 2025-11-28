import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import usuario
from usuario import Usuario
from usuario import Visitante
from usuario import Artista
from usuario import Moderador

class FakeCursor:
    def __init__(self):
        self.executed = []
        self.lastrowid = 100
        self._fetchone_data = None
        self._fetchall_data = None
        self.rowcount = 1

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
        return self.cursor_obj

    def commit(self):
        pass

    def close(self):
        pass


def fake_get_conn():
    return FakeConnection()

def test_crear_usuario(monkeypatch):
    conn = fake_get_conn()

    #simular fecha_registro del SELECT
    conn.cursor_obj._fetchone_data = ("2025-01-01 12:00:00",)

    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    user = Usuario.crear(
        nombre="Juan",
        email="juan@example.com",
        password="1234",
        rol="VISITANTE"
    )

    #validación de datos
    assert user.id == 100
    assert user.nombre == "Juan"
    assert user.email == "juan@example.com"
    assert user.rol == "VISITANTE"

    insert_query, insert_params = conn.cursor_obj.executed[0]
    assert "INSERT INTO usuarios" in insert_query
    assert insert_params[0] == "Juan"


def test_crear_usuario_rol_invalido():
    try:
        Usuario.crear("X", "x@x", "pw", "ADMIN")
        assert False, "Debe lanzar ValueError"
    except ValueError:
        assert True



def test_autenticar_correcto(monkeypatch):
    conn = fake_get_conn()

    #datos simulados de SELECT * FROM usuarios WHERE email=...
    conn.cursor_obj._fetchone_data = (
        10,                       #id
        "Maria",                  #nombre
        "maria@example.com",      #email
        usuario.hash_password("abcd"),  #password_hash
        "2025-01-01 12:00:00",    #fecha_registro
        "VISITANTE"               #rol
    )

    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    u = Usuario.autenticar("maria@example.com", "abcd")

    assert u is not None
    assert u.id == 10
    assert u.nombre == "Maria"
    assert u.rol == "VISITANTE"


def test_autenticar_usuario_no_existe(monkeypatch):
    conn = fake_get_conn()
    conn.cursor_obj._fetchone_data = None

    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    u = Usuario.autenticar("nada@example.com", "pw")
    assert u is None


def test_autenticar_password_incorrecto(monkeypatch):
    conn = fake_get_conn()

    conn.cursor_obj._fetchone_data = (
        5, "Luis", "luis@example.com",
        usuario.hash_password("correcta"),
        "2025-01-02 10:00:00", "VISITANTE"
    )

    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    u = Usuario.autenticar("luis@example.com", "incorrecta")
    assert u is None



def test_listar_todos(monkeypatch):
    conn = fake_get_conn()

    conn.cursor_obj._fetchall_data = [
        (1, "A", "a@mail", "2025-01-01", "VISITANTE"),
        (2, "B", "b@mail", "2025-01-02", "ARTISTA"),
    ]

    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    lista = Usuario.listar_todos()

    assert len(lista) == 2
    assert lista[0].nombre == "A"
    assert lista[1].rol == "ARTISTA"



def test_crear_instancia_devuelve_subclase(monkeypatch):
    """
    Cuando me envíes las subclases, esto lo completamos.
    Por ahora solo valida que no explota y devuelve un Usuario.
    """
    u = Usuario._crear_instancia(1, "X", "x@mail", None, None, "VISITANTE")
    assert isinstance(u, Usuario)


#------------------- visitante -----------------
def test_visitante_agregar_favorito(monkeypatch):
    conn = fake_get_conn()
    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    v = Visitante(1, "Juan", "j@mail", None, None, "VISITANTE")

    v.agregar_favorito(obra_id=50)

    query, params = conn.cursor_obj.executed[0]
    assert "INSERT INTO visitantes_favoritos" in query
    assert params == (1, 50)


def test_visitante_listar_favoritos(monkeypatch):
    conn = fake_get_conn()
    cur = conn.cursor_obj

    #devuelve lista de favoritos
    cur._fetchall_data = [(10,), (20,)]

    def fake_fetchall_step():
        if fake_fetchall_step.counter == 0:
            fake_fetchall_step.counter += 1
            return [(10,), (20,)]
        else:
            return [
                (10, "Obra X", 2, "Desc X"),
                (20, "Obra Y", 3, "Desc Y"),
            ]
    fake_fetchall_step.counter = 0

    cur.fetchall = fake_fetchall_step

    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    v = Visitante(1, "Ana", "a@mail", None, None, "VISITANTE")

    obras = v.listar_favoritos()
    assert len(obras) == 2
    assert obras[0][0] == 10
    assert obras[1][1] == "Obra Y"


def test_visitante_eliminar_favorito(monkeypatch):
    conn = fake_get_conn()
    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    v = Visitante(1, "Luis", "l@mail", None, None, "VISITANTE")

    v.eliminar_favorito(obra_id=77)

    query, params = conn.cursor_obj.executed[0]
    assert "DELETE FROM visitantes_favoritos" in query
    assert params == (1, 77)


def test_visitante_agregar_comentario(monkeypatch):
    class FakeComentarios:
        def crear_comentario(obra_id, usuario_id, texto):
            return ("OK", obra_id, usuario_id, texto)

    monkeypatch.setattr(usuario, "Comentarios", FakeComentarios)

    v = Visitante(2, "J", "j@mail", None, None, "VISITANTE")

    r = v.agregar_comentario(50, "Hola")
    assert r == ("OK", 50, 2, "Hola")


def test_visitante_eliminar_comentario(monkeypatch):
    conn = fake_get_conn()
    cur = conn.cursor_obj

    #SELECT autor_id FROM comentarios ...
    cur._fetchone_data = (5,)

    class FakeComentarios:
        called = False
        def eliminar_comentario_por_id(cid):
            FakeComentarios.called = True

    monkeypatch.setattr(usuario, "get_conn", lambda: conn)
    monkeypatch.setattr(usuario, "Comentarios", FakeComentarios)

    v = Visitante(5, "A", "a@mail", None, None, "VISITANTE")

    r = v.eliminar_comentario(10)

    assert r is True
    assert FakeComentarios.called is True


def test_visitante_eliminar_comentario_no_autor(monkeypatch):
    conn = fake_get_conn()
    cur = conn.cursor_obj

    cur._fetchone_data = (8,)  #es otro usuario

    class FakeComentarios:
        called = False
        def eliminar_comentario_por_id(cid):
            FakeComentarios.called = True

    monkeypatch.setattr(usuario, "get_conn", lambda: conn)
    monkeypatch.setattr(usuario, "Comentarios", FakeComentarios)

    v = Visitante(5, "A", "a@mail", None, None, "VISITANTE")

    r = v.eliminar_comentario(50)

    assert r is False
    assert FakeComentarios.called is False


def test_visitante_crear_reporte(monkeypatch):
    class FakeReportes:
        def crear_reporte(obra_id, uid, motivo):
            return ("REPORTE", obra_id, uid, motivo)

    monkeypatch.setattr(usuario, "Reportes", FakeReportes)

    v = Visitante(3, "X", "x@mail", None, None, "VISITANTE")

    r = v.crear_reporte(100, "spam")
    assert r == ("REPORTE", 100, 3, "spam")


def test_visitante_crear_sala(monkeypatch):
    class FakeSalas:
        def crear_sala(uid, nombre, descripcion, privacidad, codigo):
            return ("SALA", uid, nombre, privacidad)

    monkeypatch.setattr(usuario, "Salas", FakeSalas)

    v = Visitante(4, "Y", "y@mail", None, None, "VISITANTE")

    r = v.crear_sala("Sala 1", "desc", "PUBLICA", None)

    assert r[0] == "SALA"
    assert r[1] == 4


def test_visitante_eliminar_sala(monkeypatch):
    conn = fake_get_conn()
    conn.cursor_obj._fetchone_data = (9,)

    class FakeSalas:
        called = False
        def eliminar_sala_por_id(sid):
            FakeSalas.called = True

    monkeypatch.setattr(usuario, "get_conn", lambda: conn)
    monkeypatch.setattr(usuario, "Salas", FakeSalas)

    v = Visitante(9, "Z", "z@mail", None, None, "VISITANTE")

    r = v.eliminar_sala(55)

    assert r is True
    assert FakeSalas.called is True


def test_visitante_entrar_sala(monkeypatch):
    class SalaFake:
        def __init__(self):
            self.privacidad = "PRIVADA"
            self.codigo_acceso = "123"

    class FakeSalas:
        def obtener_sala_por_id(sid):
            return SalaFake()

    monkeypatch.setattr(usuario, "Salas", FakeSalas)

    v = Visitante(7, "U", "u@mail", None, None, "VISITANTE")

    sala = v.entrar_sala_id(1, "123")
    assert sala is not None


def test_visitante_entrar_sala_codigo_incorrecto(monkeypatch):
    class SalaFake:
        def __init__(self):
            self.privacidad = "PRIVADA"
            self.codigo_acceso = "999"

    class FakeSalas:
        def obtener_sala_por_id(sid):
            return SalaFake()

    monkeypatch.setattr(usuario, "Salas", FakeSalas)

    v = Visitante(7, "U", "u@mail", None, None, "VISITANTE")

    sala = v.entrar_sala_id(1, "000")
    assert sala is None

#---------- Artista ---------------
def test_artista_agregar_biografia(monkeypatch):
    conn = fake_get_conn()
    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    a = Artista(10, "Art", "a@mail", None, None, "ARTISTA")
    a.agregar_biografia("Soy un artista.")

    query, params = conn.cursor_obj.executed[0]
    assert "INSERT INTO artistas_info" in query
    assert params == (10, "Soy un artista.")


def test_artista_cambiar_biografia(monkeypatch):
    conn = fake_get_conn()
    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    a = Artista(11, "B", "b@mail", None, None, "ARTISTA")
    a.cambiar_biografia("Nueva bio.")

    query, params = conn.cursor_obj.executed[0]
    assert "UPDATE artistas_info" in query
    assert params == ("Nueva bio.", 11)


def test_artista_obtener_biografia(monkeypatch):
    conn = fake_get_conn()
    conn.cursor_obj._fetchone_data = ("Bio secreta",)
    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    a = Artista(12, "C", "c@mail", None, None, "ARTISTA")

    bio = a.obtener_biografia()
    assert bio == "Bio secreta"


def test_artista_obtener_biografia_no_existe(monkeypatch):
    conn = fake_get_conn()
    conn.cursor_obj._fetchone_data = None
    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    a = Artista(13, "D", "d@mail", None, None, "ARTISTA")

    bio = a.obtener_biografia()
    assert bio is None


def test_artista_ver_portafolio(monkeypatch):
    conn = fake_get_conn()
    conn.cursor_obj._fetchall_data = [
        (1, "Obra A", "Desc A"),
        (2, "Obra B", "Desc B"),
    ]
    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    a = Artista(99, "Art", "art@mail", None, None, "ARTISTA")

    obras = a.ver_portafolio()

    assert len(obras) == 2
    assert obras[0][1] == "Obra A"
    assert obras[1][2] == "Desc B"


def test_artista_agregar_obra(monkeypatch):
    class FakeObras:
        def crear_obra(t, d, uid, archivo, mini, tags, estado):
            return ("CREADA", t, uid, estado)

    monkeypatch.setattr(usuario, "Obras", FakeObras)

    a = Artista(20, "Pepe", "p@mail", None, None, "ARTISTA")

    r = a.agregar_obra("Titulo", "Desc", None, None, ["X"], "PENDIENTE")

    assert r[0] == "CREADA"
    assert r[1] == "Titulo"
    assert r[2] == 20


def test_artista_eliminar_obra(monkeypatch):
    conn = fake_get_conn()
    conn.cursor_obj._fetchone_data = (15,)

    class FakeObras:
        called = False
        def eliminar_obra_por_id(oid):
            FakeObras.called = True

    monkeypatch.setattr(usuario, "get_conn", lambda: conn)
    monkeypatch.setattr(usuario, "Obras", FakeObras)

    a = Artista(15, "A", "a@mail", None, None, "ARTISTA")

    r = a.eliminar_obra(100)

    assert r is True
    assert FakeObras.called is True


def test_artista_eliminar_obra_no_autor(monkeypatch):
    conn = fake_get_conn()
    conn.cursor_obj._fetchone_data = (99,)  # otro autor

    class FakeObras:
        called = False
        def eliminar_obra_por_id(oid):
            FakeObras.called = True

    monkeypatch.setattr(usuario, "get_conn", lambda: conn)
    monkeypatch.setattr(usuario, "Obras", FakeObras)

    a = Artista(22, "X", "x@mail", None, None, "ARTISTA")

    r = a.eliminar_obra(200)

    assert r is False
    assert FakeObras.called is False

#---------- Moderador -------------

def test_moderador_aprobar_obra(monkeypatch):
    class FakeObras:
        called = False
        args = None
        def actualizar_estado_publicacion(oid, estado):
            FakeObras.called = True
            FakeObras.args = (oid, estado)

    monkeypatch.setattr(usuario, "Obras", FakeObras)

    m = Moderador(1, "Mod", "m@mail", None, None, "MODERADOR")
    m.aprobar_obra(50)

    assert FakeObras.called is True
    assert FakeObras.args == (50, "APROBADA")


def test_moderador_rechazar_obra(monkeypatch):
    class FakeObras:
        called = False
        args = None
        def actualizar_estado_publicacion(oid, estado):
            FakeObras.called = True
            FakeObras.args = (oid, estado)

    monkeypatch.setattr(usuario, "Obras", FakeObras)

    m = Moderador(2, "Mod2", "m2@mail", None, None, "MODERADOR")
    m.rechazar_obra(80)

    assert FakeObras.called is True
    assert FakeObras.args == (80, "RECHAZADA")


def test_moderador_ver_reportes(monkeypatch):
    class FakeReportes:
        def obtener_reportes_pendientes():
            return ["R1", "R2"]

    monkeypatch.setattr(usuario, "Reportes", FakeReportes)

    m = Moderador(3, "Z", "z@mail", None, None, "MODERADOR")
    r = m.ver_reportes()

    assert r == ["R1", "R2"]


def test_moderador_resolver_reporte_borrar_obra(monkeypatch):
    conn = fake_get_conn()
    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    class FakeObras:
        called = False
        def eliminar_obra_por_id(oid):
            FakeObras.called = True

    class FakeReportes:
        called = False
        def resolver_reporte(rid):
            FakeReportes.called = True

    monkeypatch.setattr(usuario, "Obras", FakeObras)
    monkeypatch.setattr(usuario, "Reportes", FakeReportes)

    m = Moderador(10, "M", "m@mail", None, None, "MODERADOR")

    m.resolver_reporte_borrar_obra(reporte_id=5, obra_id=99)

    assert FakeObras.called is True
    assert FakeReportes.called is True

    #validar inserción en moderadores_reportes
    query, params = conn.cursor_obj.executed[-1]
    assert "INSERT INTO moderadores_reportes" in query
    assert params == (10, 5)


def test_moderador_resolver_reporte_ignorar(monkeypatch):
    conn = fake_get_conn()
    monkeypatch.setattr(usuario, "get_conn", lambda: conn)

    class FakeReportes:
        called = False
        def resolver_reporte(rid):
            FakeReportes.ca
