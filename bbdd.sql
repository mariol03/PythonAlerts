CREATE DATABASE `backups`;

CREATE TABLE `iperious_backup` (
  `hostname` varchar(45) NOT NULL,
  `Nombre_Trabajo` varchar(200) NOT NULL,
  `Ficheros_Copiados` int(11) DEFAULT NULL,
  `Ficheros_Fallidos` int(11) DEFAULT NULL,
  `Dia` date NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`hostname`,`Nombre_Trabajo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


CREATE TABLE `equipos` (
  `idEquipo` int(11) NOT NULL AUTO_INCREMENT,
  `NombreEquipo` varchar(45) COLLATE utf8mb4_unicode_ci NOT NULL,
  `NombreUsuario` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `NombreDominio` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `IdNombre` int(11) DEFAULT NULL,
  PRIMARY KEY (`idEquipo`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `alertas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nivel` int(11) NOT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `Mensaje` varchar(256) COLLATE utf8mb4_unicode_ci NOT NULL,
  `color` varchar(9) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `resuelto` tinyint(4) DEFAULT '0',
  `equipo` varchar(45) COLLATE utf8mb4_unicode_ci DEFAULT 'Todos',
  `privado` tinyint(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48986 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;



