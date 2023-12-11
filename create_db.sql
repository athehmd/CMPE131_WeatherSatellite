CREATE DATABASE `weather_satellite`;

USE `weather_satellite`;

CREATE TABLE `Data` (
    `Data` INT NULL,
    `Date` DATETIME NOT NULL,
    `Author` VARCHAR(50) NOT NULL DEFAULT ''
);
