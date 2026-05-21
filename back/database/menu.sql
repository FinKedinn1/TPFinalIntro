CREATE DATABASE IF NOT EXISTS restaurante_medieval;

USE restaurante_medieval;

CREATE TABLE carta (
    id_plato INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre_plato VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2),
    categoria VARCHAR(100),
    stock BOOLEAN DEFAULT TRUE
);

INSERT INTO carta
(nombre_plato, descripcion, precio, categoria)
VALUES

(
'Hamburguesa del Rey',
'Hamburguesa saludable con pan integral',
8500,
'Plato Principal'
),

(
'Papas del Castillo',
'Papas rusticas con especias medievales',
4200,
'Entradas'
),

(
'Poción Frutal',
'Jugo natural de frutos rojos',
3000,
'Bebidas'
),

(
'Tarta del Guerrero',
'Tarta integral de manzana',
3900,
'Postres'
);