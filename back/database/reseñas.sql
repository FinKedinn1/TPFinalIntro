CREATE DATABASE IF NOT EXISTS restaurante_medieval;

USE restaurante_medieval;

CREATE TABLE IF NOT EXISTS reseñas (
    id_reseña INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    comentario TEXT NOT NULL,
    puntaje INT CHECK (puntaje >= 1 AND puntaje <= 5),
    FOREIGN KEY (id_reserva)
    REFERENCES reservas(id_reserva)
);