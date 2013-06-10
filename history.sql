SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

CREATE SCHEMA IF NOT EXISTS `role_model` DEFAULT CHARACTER SET utf8 ;
USE `role_model` ;

-- -----------------------------------------------------
-- Table `role_model`.`entry`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `role_model`.`entry` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `author` VARCHAR(30) NULL DEFAULT NULL ,
  `file_url` VARCHAR(80) NULL DEFAULT NULL ,
  `add_time` DATETIME NULL DEFAULT NULL ,
  `istop` TINYINT(4) NULL DEFAULT NULL ,
  `count` INT(11) NULL DEFAULT NULL ,
  `entryname` VARCHAR(45) NULL DEFAULT NULL ,
  `description` TEXT NULL DEFAULT NULL ,
  `status` TINYINT(4) NULL DEFAULT NULL ,
  `area` VARCHAR(45) NULL DEFAULT NULL ,
  `keywords` VARCHAR(80) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `role_model`.`privilege`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `role_model`.`privilege` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `resource` VARCHAR(45) NULL DEFAULT NULL ,
  `operation` VARCHAR(45) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = MyISAM
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `role_model`.`role`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `role_model`.`role` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `rolename` VARCHAR(45) NULL DEFAULT NULL ,
  `description` VARCHAR(100) NULL DEFAULT NULL ,
  `add_time` DATETIME NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = MyISAM
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `role_model`.`role_inherit`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `role_model`.`role_inherit` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `from_role` VARCHAR(40) NULL DEFAULT NULL ,
  `to_role` VARCHAR(40) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = MyISAM
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `role_model`.`role_privilege_assignment`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `role_model`.`role_privilege_assignment` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `role` VARCHAR(30) NULL DEFAULT NULL ,
  `privilege` INT(11) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = MyISAM
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `role_model`.`user`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `role_model`.`user` (
  `id` INT(11) NOT NULL AUTO_INCREMENT ,
  `username` VARCHAR(45) NULL DEFAULT NULL ,
  `password` VARCHAR(45) NULL DEFAULT NULL ,
  `status` TINYINT(4) NULL DEFAULT NULL ,
  `add_time` DATETIME NULL DEFAULT NULL ,
  `rolename` VARCHAR(45) NULL DEFAULT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = MyISAM
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
