# usuarios.py
import logging
from db_connection import get_conn
import hashlib
from obras import Obras
from comentarios import Comentarios
from reportes import Reportes
from salas import Salas

logging.basicConfig(level=logging.ERROR)

def hash_password(password: str) -> str:
    if password is None:
        return None
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

ROLES_VALIDOS = {"VISITANTE", "ARTISTA", "MODERADOR"}

class Usuario:
    def __init__(self, id_, nombre, email, password_hash, fecha_registro ,rol='VISITANTE'):
        if rol not in ROLES_VALIDOS:
            raise ValueError(f"Rol inválido: {rol}")
        self.id = id_
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash
        self.fecha_registro = fecha_registro
        self.rol = rol


    #instancias
    @staticmethod
    def _crear_instancia(id_, nombre, email, password_hash, fecha_registro, rol):
        """Devuelve la subclase correcta según rol."""
        if rol == "VISITANTE":
            return Visitante(id_, nombre, email, password_hash, fecha_registro, rol)
        if rol == "ARTISTA":
            return Artista(id_, nombre, email, password_hash, fecha_registro, rol)
        if rol == "MODERADOR":
            return Moderador(id_, nombre, email, password_hash, fecha_registro, rol)
        return Usuario(id_, nombre, email, password_hash, fecha_registro, rol)




    #crear usuario

    @classmethod
    def crear(cls, nombre, email, password, rol='VISITANTE'):
        if rol not in ROLES_VALIDOS:
            raise ValueError(f"Rol inválido: {rol}")
        conn = get_conn()
        try:
            cur = conn.cursor()
            pwd_hash = hash_password(password)
            cur.execute(
                "INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES (%s, %s, %s, %s)",
                (nombre, email, pwd_hash, rol)
            )
            conn.commit()

            uid = cur.lastrowid
            cur.execute("SELECT fecha_registro FROM usuarios WHERE id = %s", (uid,))
            fecha = cur.fetchone()[0]

            return cls._crear_instancia(uid, nombre, email, pwd_hash, fecha, rol)
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al crear usuario:", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    #revisar contraseña
    @classmethod
    def autenticar(cls, email, password):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nombre, email, password_hash, fecha_registro, rol
                FROM usuarios
                WHERE email = %s
            """, (email,))
            
            fila = cur.fetchone()
            #si no se encuentra el usuario
            if not fila:
                return None

            stored_hash = fila[3]
            #verificar contraseña
            if hash_password(password) != stored_hash:
                return None

            return cls._crear_instancia(
                fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]
            )
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al autenticar", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def listar_todos(cls):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id, nombre, email, fecha_registro, rol FROM usuarios")
            rows = cur.fetchall()
            return [
                cls(
                    id_=r[0],
                    nombre=r[1],
                    email=r[2],
                    password_hash=None,
                    fecha_registro=r[3],
                    rol=r[4]
                )
                for r in rows
            ]
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al listar usuarios", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_por_id(cls, usuario_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nombre, email, password_hash, fecha_registro, rol
                FROM usuarios
                WHERE id = %s
            """, (usuario_id,))
            fila = cur.fetchone()
            if not fila:
                return None

            return cls._crear_instancia(
                fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]
            )
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al obtener usuario por ID", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_por_email(cls, email):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("""
                SELECT id, nombre, email, password_hash, fecha_registro, rol
                FROM usuarios
                WHERE email = %s
            """, (email,))
            fila = cur.fetchone()
            if not fila:
                return None

            return cls._crear_instancia(
                fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]
            )
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al obtener usuario por email", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def get_rol_por_ID(cls, usuario_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT rol FROM usuarios WHERE id = %s", (usuario_id,))
            fila = cur.fetchone()
            if fila:
                return fila[0]
            return None
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al obtener rol", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_rol_por_email(cls, email):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT rol FROM usuarios WHERE email = %s", (email,))
            fila = cur.fetchone()
            if fila:
                return fila[0]
            return None
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al obtener rol por email", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @classmethod
    def obtener_id_por_email(cls, email):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            fila = cur.fetchone()
            if fila:
                return fila[0]
            return None
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al obtener ID por email", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()
    
    def __str__(self):
        return f"{self.nombre} ({self.rol})"
    
    @classmethod
    def obtener_nombre_por_id(cls, usuario_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("SELECT nombre FROM usuarios WHERE id = %s", (usuario_id,))
            fila = cur.fetchone()
            if fila:
                return fila[0]
            return None
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al obtener nombre por ID", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()    


#subclases

class Visitante(Usuario):
    def agregar_favorito(self, obra_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO visitantes_favoritos (usuario_id, obra_id) VALUES (%s, %s)",
                (self.id, obra_id)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al agregar favorito", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    def listar_favoritos(self):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT obra_id FROM visitantes_favoritos WHERE usuario_id = %s",
                (self.id,)
            )
            filas = cur.fetchall()
            if not filas:
                return []
            cur.execute(
                "SELECT id, titulo, autor_id, descripcion FROM obras WHERE id IN (%s)" %
                ','.join(['%s'] * len(filas)),
                tuple(fila[0] for fila in filas)
            )
            obras = cur.fetchall()
            return obras
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al listar favoritos", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()
    
    def eliminar_favorito(self, obra_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM visitantes_favoritos WHERE usuario_id = %s AND obra_id = %s",
                (self.id, obra_id)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al eliminar favorito", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()
    
    def agregar_comentario(self, obra_id, texto):
        return Comentarios.crear_comentario(obra_id, self.id, texto)  

    def eliminar_comentario(self, comentario_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT autor_id FROM comentarios WHERE id = %s",
                (comentario_id,)
            )
            autor_id = cur.fetchone()
            if autor_id and autor_id[0] == self.id:
                Comentarios.eliminar_comentario_por_id(comentario_id)
                conn.commit()
                return True
            return False
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al eliminar comentario", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    def crear_reporte(self, obra_id, motivo):
        return Reportes.crear_reporte(obra_id, self.id, motivo)
    
    def crear_sala(self, nombre, descripcion, privacidad, codigo_acceso):
        return Salas.crear_sala(self.id, nombre, descripcion, privacidad, codigo_acceso)
    
    def eliminar_sala(self, sala_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT autor_id FROM salas WHERE id = %s",
                (sala_id,)
            )
            autor_id = cur.fetchone()
            if autor_id and autor_id[0] == self.id:
                Salas.eliminar_sala_por_id(sala_id)
                conn.commit()
                return True
            return False
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al eliminar sala", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    def entrar_sala_id(self, sala_id, codigo_acceso):
        sala = Salas.obtener_sala_por_id(sala_id)
        if sala is None:
            return None
        if sala.privacidad == 'PRIVADA':
            if sala.codigo_acceso != codigo_acceso:
                return None
        return sala

class Artista(Usuario):
    @staticmethod
    def agregar_biografia(usuario_id, biografia):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO artistas_info (usuario_id, biografia) VALUES (%s, %s)",
                (usuario_id, biografia)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al agregar biografia", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @staticmethod
    def cambiar_biografia(usuario_id, biografia):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE artistas_info SET biografia = %s WHERE usuario_id = %s",
                (biografia, usuario_id)
            )
            conn.commit()
            return True

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al cambiar biografia", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()
        
    @staticmethod
    def obtener_biografia(usuario_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT biografia FROM artistas_info WHERE usuario_id = %s",
                (usuario_id,)
            )
            fila = cur.fetchone()
            if fila:
                return fila[0]
            return None
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al obtener biografia", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    @staticmethod
    def ver_portafolio(usuario_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, titulo, descripcion FROM obras WHERE autor_id = %s",
                (usuario_id,)
            )
            obras = cur.fetchall()
            return obras
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al ver portafolio", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    def agregar_obra(self, titulo, descripcion, archivo_url=None, miniatura_url=None, tags=[], estado_publicacion="PENDIENTE"):
        return Obras.crear_obra(titulo, descripcion, self.id, archivo_url, miniatura_url, tags, estado_publicacion)
    
    def eliminar_obra(self, obra_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("select autor_id from obras where id = %s", (obra_id,))
            autor_id = cur.fetchone()
            if autor_id and autor_id[0] == self.id:
                Obras.eliminar_obra_por_id(obra_id)
                conn.commit()
                return True
            return False
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al eliminar obra", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()


class Moderador(Usuario):
    def aprobar_obra(self, obra_id):
        Obras.actualizar_estado_publicacion(obra_id, "APROBADA")

    def rechazar_obra(self, obra_id):
        Obras.actualizar_estado_publicacion(obra_id, "RECHAZADA")
    
    def ver_reportes(self):
        return Reportes.obtener_reportes_pendientes()

    def resolver_reporte_borrar_obra(self, reporte_id, obra_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            #eliminar la obra
            Obras.eliminar_obra_por_id(obra_id)
            #actualizar el estado del reporte
            Reportes.resolver_reporte(reporte_id)
            #añadir reporte resuelto por el moderador
            cur.execute(
                "INSERT INTO moderadores_reportes (moderador_id, reporte_id) VALUES (%s, %s)",
                (self.id, reporte_id)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al resolver reporte y borrar obra", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()
    
    def resolver_reporte_ignorar(self, reporte_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            #actualizar el estado del reporte
            Reportes.resolver_reporte(reporte_id)
            cur.execute(
                "INSERT INTO moderadores_reportes (moderador_id, reporte_id) VALUES (%s, %s)",
                (self.id, reporte_id)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al resolver reporte ignorando", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    def listar_bloqueados(self):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT usuario_bloqueado_id FROM moderadores_bloqueos WHERE moderador_id = %s",
                (self.id,)
            )
            filas = cur.fetchall()
            bloqueados = [fila[0] for fila in filas]
            return bloqueados
        
        except Exception as e:
            conn.rollback()
            logging.error(f"Error al listar bloqueados", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()
    
    def bloquear_usuario(self, usuario_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO moderadores_bloqueos (moderador_id, usuario_bloqueado_id) VALUES (%s, %s)",
                (self.id, usuario_id)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al bloquear usuario", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    def desbloquear_usuario(self, usuario_id):
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "DELETE FROM moderadores_bloqueos WHERE moderador_id = %s AND usuario_bloqueado_id = %s",
                (self.id, usuario_id)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            logging.error(f"Error al desbloquear usuario", exc_info=True)
            raise

        finally:
            cur.close()
            conn.close()

    

