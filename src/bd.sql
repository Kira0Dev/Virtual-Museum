
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    fecha_registro  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rol ENUM('VISITANTE', 'ARTISTA', 'MODERADOR') DEFAULT 'VISITANTE'
);

CREATE TABLE obras (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descripcion TEXT,
    autor_id INT,
    archivo_url TEXT NOT NULL,
    miniatura_url TEXT NOT NULL,
    tags JSON,
    estado_publicacion ENUM('BORRADOR', 'PENDIENTE', 'PUBLICADO', 'RECHAZADA') DEFAULT 'PENDIENTE',
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    contador_likes INT DEFAULT 0,
    FOREIGN KEY (autor_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE visitantes_favoritos (
usuario_id INT,
    obra_id INT,
    PRIMARY KEY (usuario_id, obra_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE,
    FOREIGN KEY (obra_id) REFERENCES obras(id)
        ON DELETE CASCADE
);


CREATE TABLE artistas_info (
    usuario_id INT PRIMARY KEY,
    biografia TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE artistas_portafolio (
    usuario_id INT,
    obra_id INT,
    PRIMARY KEY (usuario_id, obra_id),
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        ON DELETE CASCADE,
    FOREIGN KEY (obra_id) REFERENCES obras(id)
        ON DELETE CASCADE
);

CREATE TABLE reportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    obra_id INT,
    autor_id INT,
    motivo TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('REVISION', 'RESUELTO') DEFAULT 'REVISION',
    FOREIGN KEY (obra_id) REFERENCES obras(id)
        ON DELETE CASCADE,
    FOREIGN KEY (autor_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE moderadores_bloqueos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    moderador_id INT,
    usuario_bloqueado_id INT,
    motivo VARCHAR(255),
    fecha_bloqueo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (moderador_id) REFERENCES usuarios(id)
        ON DELETE CASCADE,
    FOREIGN KEY (usuario_bloqueado_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE moderadores_reportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    moderador_id INT,
    reporte_id INT,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (moderador_id) REFERENCES usuarios(id)
        ON DELETE CASCADE,
    FOREIGN KEY (reporte_id) REFERENCES reportes(id)
        ON DELETE CASCADE
);

CREATE TABLE comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    obra_id INT,
    autor_id INT,
    texto TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('VISIBLE', 'REPORTADO', 'ELIMINADO') DEFAULT 'VISIBLE',
    FOREIGN KEY (obra_id) REFERENCES obras(id)
        ON DELETE CASCADE,
    FOREIGN KEY (autor_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE salas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    autor_id INT,
    nombre VARCHAR(120) NOT NULL,
    descripcion TEXT,
    privacidad ENUM('PUBLICA', 'PRIVADA') DEFAULT 'PUBLICA',
    codigo_acceso VARCHAR(50),
    FOREIGN KEY (autor_id) REFERENCES usuarios(id)
        ON DELETE CASCADE
);

CREATE TABLE salas_obras (
    sala_id INT,
    obra_id INT,
    PRIMARY KEY (sala_id, obra_id),
    FOREIGN KEY (sala_id) REFERENCES salas(id)
        ON DELETE CASCADE,
    FOREIGN KEY (obra_id) REFERENCES obras(id)
        ON DELETE CASCADE
);