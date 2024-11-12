-- Active: 1727790809895@@127.0.0.1@3306@db_amy
CREATE DATABASE db_amy;

USE db_amy;

CREATE TABLE formacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_escuela VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    detalles TEXT NOT NULL
);

CREATE TABLE experiencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empresa VARCHAR(255) NOT NULL,
    puesto VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE,  -- Puede ser nulo si sigue vigente
    detalles TEXT
);

CREATE TABLE aptitud (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    nivel VARCHAR(50) NOT NULL,
    detalles TEXT
);

CREATE TABLE infor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    foto_perfil LONGBLOB,  -- Campo para la foto de perfil
    contacto TEXT,
    ubicacion TEXT,
    idioma TEXT,
    correo VARCHAR(50),
    telefono VARCHAR(20),
    descripcion TEXT
);

CREATE TABLE contacto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    mensaje TEXT NOT NULL
);