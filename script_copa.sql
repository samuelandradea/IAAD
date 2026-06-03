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
