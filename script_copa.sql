-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema Copa do Mundo de Futebol
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `Copa do Mundo de Futebol` ;

-- -----------------------------------------------------
-- Schema Copa do Mundo de Futebol
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `Copa do Mundo de Futebol` DEFAULT CHARACTER SET utf8 ;
USE `Copa do Mundo de Futebol` ;

-- -----------------------------------------------------
-- Table `Copa do Mundo de Futebol`.`Selecoes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Copa do Mundo de Futebol`.`Selecoes` (
  `id_selecoes` INT NOT NULL,
  `nome_selecao` VARCHAR(50) NOT NULL,
  `continente` VARCHAR(30) NOT NULL,
  `tecnico` VARCHAR(50) NOT NULL,
  `titulos` INT NOT NULL,
  PRIMARY KEY (`id_selecoes`),
  UNIQUE INDEX `nome_selecao_UNIQUE` (`nome_selecao` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Copa do Mundo de Futebol`.`Jogadores`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Copa do Mundo de Futebol`.`Jogadores` (
  `id_jogador` INT NOT NULL,
  `nome_jogador` VARCHAR(60) NOT NULL,
  `posicao` VARCHAR(30) NOT NULL,
  `numero_camisa` INT NOT NULL,
  `data_nascimento` DATE NOT NULL,
  `Selecoes_id_selecoes` INT NOT NULL,
  PRIMARY KEY (`id_jogador`),
  INDEX `fk_Jogadores_Selecoes_idx` (`Selecoes_id_selecoes` ASC) VISIBLE,
  CONSTRAINT `fk_Jogadores_Selecoes`
    FOREIGN KEY (`Selecoes_id_selecoes`)
    REFERENCES `Copa do Mundo de Futebol`.`Selecoes` (`id_selecoes`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Copa do Mundo de Futebol`.`Estadios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Copa do Mundo de Futebol`.`Estadios` (
  `id_estadios` INT NOT NULL,
  `nome_estadio` VARCHAR(80) NOT NULL,
  `cidade` VARCHAR(50) NOT NULL,
  `pais` VARCHAR(50) NOT NULL,
  `capacidade` INT NOT NULL,
  PRIMARY KEY (`id_estadios`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `Copa do Mundo de Futebol`.`Partidas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Copa do Mundo de Futebol`.`Partidas` (
  `id_partida` INT NOT NULL,
  `data_partida` DATE NOT NULL,
  `quantidade_gols_selecao_1` INT NOT NULL,
  `quantidade_gols_selecao_2` INT NOT NULL,
  `id_estadio` INT NOT NULL,
  `id_selecao_1` INT NOT NULL,
  `id_selecao_2` INT NOT NULL,
  `vencedor` INT NULL,
  PRIMARY KEY (`id_partida`),
  INDEX `fk_Partidas_Estadios1_idx` (`id_estadio` ASC) VISIBLE,
  INDEX `fk_Partidas_Selecoes1_idx` (`id_selecao_1` ASC) VISIBLE,
  INDEX `fk_Partidas_Selecoes2_idx` (`id_selecao_2` ASC) VISIBLE,
  INDEX `fk_Partidas_Selecoes3_idx` (`vencedor` ASC) VISIBLE,
  CONSTRAINT `fk_Partidas_Estadios1`
    FOREIGN KEY (`id_estadio`)
    REFERENCES `Copa do Mundo de Futebol`.`Estadios` (`id_estadios`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Partidas_Selecoes1`
    FOREIGN KEY (`id_selecao_1`)
    REFERENCES `Copa do Mundo de Futebol`.`Selecoes` (`id_selecoes`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Partidas_Selecoes2`
    FOREIGN KEY (`id_selecao_2`)
    REFERENCES `Copa do Mundo de Futebol`.`Selecoes` (`id_selecoes`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Partidas_Selecoes3`
    FOREIGN KEY (`vencedor`)
    REFERENCES `Copa do Mundo de Futebol`.`Selecoes` (`id_selecoes`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


-- =========================
-- POPULAR BANCO
-- =========================

-- =========================
-- Esse conjunto gera:

-- 10 seleções reais
-- 50 jogadores reais
-- 8 estádios oficiais da Copa 2026
-- 12 partidas para testes
-- =========================


USE `Copa do Mundo de Futebol`;

-- ==========================
-- SELEÇÕES
-- ==========================

INSERT INTO Selecoes VALUES
(1,'Brasil','América do Sul','Carlo Ancelotti',5),
(2,'Argentina','América do Sul','Lionel Scaloni',3),
(3,'França','Europa','Didier Deschamps',2),
(4,'Espanha','Europa','Luis de la Fuente',1),
(5,'Alemanha','Europa','Julian Nagelsmann',4),
(6,'Inglaterra','Europa','Thomas Tuchel',1),
(7,'Portugal','Europa','Roberto Martínez',0),
(8,'Marrocos','África','Walid Regragui',0),
(9,'Japão','Ásia','Hajime Moriyasu',0),
(10,'Estados Unidos','América do Norte','Mauricio Pochettino',0);

-- ==========================
-- JOGADORES - BRASIL
-- ==========================

INSERT INTO Jogadores VALUES
(1,'Alisson Becker','Goleiro',1,'1992-10-02',1),
(2,'Marquinhos','Zagueiro',4,'1994-05-14',1),
(3,'Gabriel Magalhães','Zagueiro',3,'1997-12-19',1),
(4,'Bruno Guimarães','Meio-Campo',8,'1997-11-16',1),
(5,'Vinicius Junior','Atacante',7,'2000-07-12',1);

-- ARGENTINA

INSERT INTO Jogadores VALUES
(6,'Emiliano Martinez','Goleiro',23,'1992-09-02',2),
(7,'Cristian Romero','Zagueiro',13,'1998-04-27',2),
(8,'Lisandro Martinez','Zagueiro',25,'1998-01-18',2),
(9,'Enzo Fernandez','Meio-Campo',24,'2001-01-17',2),
(10,'Julian Alvarez','Atacante',9,'2000-01-31',2);

-- FRANÇA

INSERT INTO Jogadores VALUES
(11,'Mike Maignan','Goleiro',1,'1995-07-03',3),
(12,'William Saliba','Zagueiro',17,'2001-03-24',3),
(13,'Jules Kounde','Zagueiro',5,'1998-11-12',3),
(14,'Aurelien Tchouameni','Meio-Campo',8,'2000-01-27',3),
(15,'Kylian Mbappe','Atacante',10,'1998-12-20',3);

-- ESPANHA

INSERT INTO Jogadores VALUES
(16,'Unai Simon','Goleiro',23,'1997-06-11',4),
(17,'Robin Le Normand','Zagueiro',3,'1996-11-11',4),
(18,'Pau Cubarsi','Zagueiro',2,'2007-01-22',4),
(19,'Pedri','Meio-Campo',20,'2002-11-25',4),
(20,'Lamine Yamal','Atacante',19,'2007-07-13',4);

-- ALEMANHA

INSERT INTO Jogadores VALUES
(21,'Marc Andre ter Stegen','Goleiro',1,'1992-04-30',5),
(22,'Antonio Rudiger','Zagueiro',2,'1993-03-03',5),
(23,'Jonathan Tah','Zagueiro',4,'1996-02-11',5),
(24,'Jamal Musiala','Meio-Campo',10,'2003-02-26',5),
(25,'Kai Havertz','Atacante',7,'1999-06-11',5);

-- INGLATERRA

INSERT INTO Jogadores VALUES
(26,'Jordan Pickford','Goleiro',1,'1994-03-07',6),
(27,'John Stones','Zagueiro',5,'1994-05-28',6),
(28,'Marc Guehi','Zagueiro',6,'2000-07-13',6),
(29,'Jude Bellingham','Meio-Campo',10,'2003-06-29',6),
(30,'Harry Kane','Atacante',9,'1993-07-28',6);

-- PORTUGAL

INSERT INTO Jogadores VALUES
(31,'Diogo Costa','Goleiro',1,'1999-09-19',7),
(32,'Ruben Dias','Zagueiro',3,'1997-05-14',7),
(33,'Pepe','Zagueiro',4,'1983-02-26',7),
(34,'Bruno Fernandes','Meio-Campo',8,'1994-09-08',7),
(35,'Cristiano Ronaldo','Atacante',7,'1985-02-05',7);

-- MARROCOS

INSERT INTO Jogadores VALUES
(36,'Yassine Bounou','Goleiro',1,'1991-04-05',8),
(37,'Achraf Hakimi','Lateral',2,'1998-11-04',8),
(38,'Nayef Aguerd','Zagueiro',5,'1996-03-30',8),
(39,'Sofyan Amrabat','Meio-Campo',4,'1996-08-21',8),
(40,'Hakim Ziyech','Atacante',7,'1993-03-19',8);

-- JAPÃO

INSERT INTO Jogadores VALUES
(41,'Zion Suzuki','Goleiro',1,'2002-08-21',9),
(42,'Takehiro Tomiyasu','Zagueiro',22,'1998-11-05',9),
(43,'Ko Itakura','Zagueiro',4,'1997-01-27',9),
(44,'Wataru Endo','Meio-Campo',6,'1993-02-09',9),
(45,'Takefusa Kubo','Atacante',20,'2001-06-04',9);

-- EUA

INSERT INTO Jogadores VALUES
(46,'Matt Turner','Goleiro',1,'1994-06-24',10),
(47,'Chris Richards','Zagueiro',3,'2000-03-28',10),
(48,'Tim Ream','Zagueiro',13,'1987-10-05',10),
(49,'Weston McKennie','Meio-Campo',8,'1998-08-28',10),
(50,'Christian Pulisic','Atacante',10,'1998-09-18',10);

-- ==========================
-- ESTÁDIOS OFICIAIS 2026
-- ==========================

INSERT INTO Estadios VALUES
(1,'MetLife Stadium','New Jersey','Estados Unidos',82500),
(2,'SoFi Stadium','Los Angeles','Estados Unidos',70240),
(3,'AT&T Stadium','Dallas','Estados Unidos',80000),
(4,'Mercedes-Benz Stadium','Atlanta','Estados Unidos',71000),
(5,'Estadio Azteca','Cidade do México','México',87523),
(6,'BMO Field','Toronto','Canadá',30000),
(7,'BC Place','Vancouver','Canadá',54500),
(8,'NRG Stadium','Houston','Estados Unidos',72220);

-- ==========================
-- PARTIDAS DE TESTE
-- ==========================

INSERT INTO Partidas VALUES
(1,'2026-06-12',2,1,1,1,9,1),
(2,'2026-06-13',3,2,2,2,10,2),
(3,'2026-06-14',1,1,3,3,6,NULL),
(4,'2026-06-15',2,0,4,4,8,4),
(5,'2026-06-16',1,0,5,5,7,5),
(6,'2026-06-17',2,2,6,1,2,NULL),
(7,'2026-06-18',3,1,7,3,9,3),
(8,'2026-06-19',2,1,8,6,10,6),
(9,'2026-06-20',1,0,1,7,8,7),
(10,'2026-06-21',2,2,2,4,5,NULL),
(11,'2026-06-22',3,1,3,1,10,1),
(12,'2026-06-23',2,0,4,2,9,2);
