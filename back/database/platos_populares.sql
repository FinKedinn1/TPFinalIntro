CREATE DATABASE IF NOT EXISTS restaurante_medieval;

USE restaurante_medieval;

CREATE TABLE IF NOT EXISTS platos_populares (
    id_plato_popular INT AUTO_INCREMENT PRIMARY KEY,
    id_plato INT NOT NULL,
    promedio_estrellas DECIMAL(3,2) NOT NULL DEFAULT 0.00,
    cantidad_reseñas INT NOT NULL DEFAULT 0,
    es_popular BOOLEAN NOT NULL DEFAULT FALSE,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (id_plato)
    REFERENCES carta(id_plato)
    ON DELETE CASCADE,

    UNIQUE (id_plato)
);

 INSERT INTO platos_populares (id_plato, promedio_estrellas, cantidad_reseñas, es_popular)
 VALUES
 (13, 4.5, 100, TRUE),
 (14, 4.2, 80, TRUE),
 (15, 3.5, 50, FALSE),
 (16, 4.8, 120, TRUE),
 (17, 3.0, 30, FALSE),
 (18, 3.5, 50, FALSE),
 (19, 4.8, 120, TRUE),
 (20, 3.0, 30, FALSE),
 (21, 3.0, 30, FALSE),
 (22, 3.5, 50, FALSE),
 (23, 4.8, 120, TRUE),
 (24, 3.0, 30, FALSE);