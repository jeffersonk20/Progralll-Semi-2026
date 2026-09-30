-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 21, 2026 at 08:43 PM
-- Server version: 10.4.25-MariaDB
-- PHP Version: 8.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

--
-- Database: `db_sistema_impuestos`
--

-- --------------------------------------------------------

--
-- Table structure for table `clientes`
--

CREATE TABLE `clientes` (
  `idCliente` int(10) NOT NULL,
  `codigo` char(10) NOT NULL,
  `nombre` char(100) NOT NULL,
  `direccion` char(150) NOT NULL,
  `telefono` char(10) NOT NULL,
  `email` char(150) NOT NULL,
  `tipo` char(10) NOT NULL DEFAULT 'particular'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `clientes`
--

INSERT INTO `clientes` (`idCliente`, `codigo`, `nombre`, `direccion`, `telefono`, `email`, `tipo`) VALUES
(1, '001', 'Luis Hernandez', 'Usulutan', '4545-3256', 'luishernandez@ugb.edu.sv', 'particular');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`idCliente`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `clientes`
--
ALTER TABLE `clientes`
  MODIFY `idCliente` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

-- --------------------------------------------------------

--
-- Table structure for table `periodos_actividades_economicas`
--

CREATE TABLE `periodos_actividades_economicas` (
  `idPeriodo` int(10) NOT NULL AUTO_INCREMENT,
  `idCliente` int(10) NOT NULL,
  `desde` date NOT NULL,
  `hasta` date NOT NULL,
  `balance` decimal(12,2) NOT NULL,
  `codigo` char(10) NOT NULL DEFAULT '11801',
  `precio` decimal(10,2) NOT NULL,
  `estado` varchar(30) NOT NULL DEFAULT 'Histórico',
  `precio_base` decimal(10,2) DEFAULT NULL,
  `adicional` decimal(10,2) DEFAULT NULL,
  `porcentaje` decimal(5,2) DEFAULT 0.00,
  `formula` varchar(255) DEFAULT NULL,
  `fecha_registro` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`idPeriodo`),
  KEY `fk_periodos_cliente` (`idCliente`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `periodos_actividades_economicas`
--

INSERT INTO `periodos_actividades_economicas` (`idPeriodo`, `idCliente`, `desde`, `hasta`, `balance`, `codigo`, `precio`, `estado`, `precio_base`, `adicional`, `porcentaje`, `formula`) VALUES
(1, 1, '2022-01-01', '2023-01-01', '700.00', '11801', '2.10', 'Histórico', '1.50', '3.00', '0.00', '1.50 + ((700.00 - 500.00) / 1,000 * 3.00)'),
(2, 1, '2023-01-01', '2024-01-01', '545.00', '11801', '4.50', 'Histórico', '1.50', '3.00', '0.00', '1.50 + (CEIL((545.00 - 500.01) / 1000) * 3.00)'),
(3, 1, '2024-01-01', '2025-01-01', '550.00', '11801', '4.50', 'Histórico', '1.50', '3.00', '0.00', '1.50 + (CEIL((550.00 - 500.01) / 1000) * 3.00)'),
(4, 1, '2025-01-01', '2026-01-01', '550.00', '11801', '4.50', 'Histórico', '1.50', '3.00', '0.00', '1.50 + (CEIL((550.00 - 500.01) / 1000) * 3.00)'),
(5, 1, '2026-01-01', '2027-01-01', '550.00', '11801', '4.50', 'Vigente según fecha', '1.50', '3.00', '0.00', '1.50 + (CEIL((550.00 - 500.01) / 1000) * 3.00)');

COMMIT;