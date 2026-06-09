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

USE `Copa do Mundo de Futebol`;

-- =========================
-- SELEÇÕES
-- =========================
INSERT INTO Selecoes
(id_selecoes, nome_selecao, continente, tecnico, titulos)
VALUES
(1, 'Brasil', 'America do Sul', 'Dorival Junior', 5),
(2, 'Franca', 'Europa', 'Didier Deschamps', 2),
(3, 'Marrocos', 'Africa', 'Walid Regragui', 0),
(4, 'Japao', 'Asia', 'Hajime Moriyasu', 0),
(5, 'Estados Unidos', 'America do Norte', 'Mauricio Pochettino', 0),
(6, 'Australia', 'Oceania', 'Tony Popovic', 0);

-- =========================
-- JOGADORES
-- =========================
INSERT INTO Jogadores
(id_jogador, nome_jogador, posicao, numero_camisa, data_nascimento, Selecoes_id_selecoes)
VALUES

-- Brasil
(1, 'Alisson Becker', 'Goleiro', 1, '1992-10-02', 1),
(2, 'Marquinhos', 'Zagueiro', 4, '1994-05-14', 1),
(3, 'Vinicius Junior', 'Atacante', 7, '2000-07-12', 1),

-- França
(4, 'Mike Maignan', 'Goleiro', 1, '1995-07-03', 2),
(5, 'William Saliba', 'Zagueiro', 17, '2001-03-24', 2),
(6, 'Kylian Mbappe', 'Atacante', 10, '1998-12-20', 2),

-- Marrocos
(7, 'Yassine Bounou', 'Goleiro', 1, '1991-04-05', 3),
(8, 'Achraf Hakimi', 'Lateral', 2, '1998-11-04', 3),
(9, 'Hakim Ziyech', 'Meia', 7, '1993-03-19', 3),

-- Japão
(10, 'Zion Suzuki', 'Goleiro', 1, '2002-08-21', 4),
(11, 'Takehiro Tomiyasu', 'Zagueiro', 22, '1998-11-05', 4),
(12, 'Takefusa Kubo', 'Atacante', 20, '2001-06-04', 4),

-- Estados Unidos
(13, 'Matt Turner', 'Goleiro', 1, '1994-06-24', 5),
(14, 'Christian Pulisic', 'Atacante', 10, '1998-09-18', 5),
(15, 'Weston McKennie', 'Meia', 8, '1998-08-28', 5),

-- Austrália
(16, 'Mathew Ryan', 'Goleiro', 1, '1992-04-08', 6),
(17, 'Harry Souttar', 'Zagueiro', 19, '1998-10-22', 6),
(18, 'Craig Goodwin', 'Atacante', 23, '1991-12-16', 6);

-- =========================
-- ESTÁDIOS
-- =========================
INSERT INTO Estadios
(id_estadios, nome_estadio, cidade, pais, capacidade)
VALUES
(1, 'Lusail Stadium', 'Lusail', 'Catar', 88966),
(2, 'Al Bayt Stadium', 'Al Khor', 'Catar', 68895),
(3, '974 Stadium', 'Doha', 'Catar', 44089),
(4, 'Education City Stadium', 'Al Rayyan', 'Catar', 45350);

-- =========================
-- PARTIDAS
-- =========================
INSERT INTO Partidas
(id_partida, data_partida, quantidade_gols_selecao_1,
 quantidade_gols_selecao_2, id_estadio,
 id_selecao_1, id_selecao_2, vencedor)
VALUES

(1, '2026-06-15', 3, 1, 1, 1, 4, 1), -- Brasil x Japão
(2, '2026-06-16', 2, 2, 2, 2, 5, NULL), -- França x EUA
(3, '2026-06-17', 1, 0, 3, 3, 6, 3), -- Marrocos x Austrália
(4, '2026-06-18', 2, 3, 4, 1, 2, 2), -- Brasil x França
(5, '2026-06-19', 0, 1, 1, 4, 5, 5), -- Japão x EUA
(6, '2026-06-20', 2, 2, 2, 3, 1, NULL); -- Marrocos x Brasil
