CREATE DATABASE analytic_dbm CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- DROP TABLE onus
create table onus (
	id int not null auto_increment primary key,
    NAME varchar(255) not null,
    SERIAL varchar(255) not null,
    PON varchar(10) not null,
    DBM float not null,
    ONUID varchar(4) not null,
  	CREATED_AT TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)

-- ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '965700';



create table olt_config (
  `id` int NOT NULL AUTO_INCREMENT primary key,
  `HOST` varchar(191) NOT NULL,
  `OLT_NAME` varchar(191) NOT NULL,
  `PONS` int NOT NULL DEFAULT 16,

  PRIMARY KEY (`id`)
)


CREATE TABLE `pons_average_dbm` (
  `id` int NOT NULL AUTO_INCREMENT,
  `PON` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `DBM_AVERAGE` float NOT NULL,
  `ID_OLT` int NOT NULL,

  `CREATED_AT` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
)

ALTER TABLE `pons_average_dbm` ADD FOREIGN KEY (`ID_OLT`) REFERENCES olt_config (`id`)