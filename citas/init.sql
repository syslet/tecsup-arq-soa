CREATE DATABASE salud;

USE salud;

CREATE TABLE citas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha_hora DATETIME NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    medico VARCHAR(100) NOT NULL,
    dni_paciente VARCHAR(10) NOT NULL,
    paciente VARCHAR(100) NOT NULL,
    centro_salud VARCHAR(100) NOT NULL,
    consultorio VARCHAR(50) NOT NULL,
    estado VARCHAR(20) NOT NULL
);