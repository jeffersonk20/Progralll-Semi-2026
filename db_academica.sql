-- ==========================================================
-- ARCHIVO DE EXPORTACIÓN DE BASE DE DATOS
-- PARCIAL II - PROGRAMACIÓN III
-- Estudiante: usss013125
-- Base de Datos: db_academica
-- Tabla: usuarios_usss013125
-- ==========================================================

CREATE DATABASE IF NOT EXISTS `db_academica` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `db_academica`;

-- --------------------------------------------------------
-- Estructura de tabla para la tabla `usuarios_usss013125`
-- --------------------------------------------------------

DROP TABLE IF EXISTS `usuarios_usss013125`;
CREATE TABLE `usuarios_usss013125` (
  `idUsuario` int(10) NOT NULL AUTO_INCREMENT,
  `usuario` char(35) NOT NULL,
  `clave` char(35) NOT NULL,
  `nombre` char(85) NOT NULL,
  `direccion` char(100) NOT NULL,
  `telefono` char(9) NOT NULL,
  PRIMARY KEY (`idUsuario`),
  UNIQUE KEY `idx_usuario` (`usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
-- Volcado de datos para la tabla `usuarios_usss013125`
-- --------------------------------------------------------

INSERT INTO `usuarios_usss013125` (`idUsuario`, `usuario`, `clave`, `nombre`, `direccion`, `telefono`) VALUES
(1, 'usss013125', '12345', 'Jefferson Castillo', 'Usulután, El Salvador', '7000-0000'),
(2, 'docente', 'docente123', 'Profesor Evaluador', 'San Salvador', '7123-4567');
