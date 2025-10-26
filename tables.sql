
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, 
    SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bfb_project` DEFAULT CHARACTER SET utf8mb4;
USE `bfb_project`;

-- -----------------------------------------------------
-- Table: person
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `person` (
  `person_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `cell_no` VARCHAR(45) NOT NULL,
  `nat_id` VARCHAR(45) NULL,
  `student_number` VARCHAR(45) NULL,
  PRIMARY KEY (`person_id`),
  UNIQUE INDEX `ak_nat_id` (`nat_id`),
  UNIQUE INDEX `ak_student_number` (`student_number`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table: restaurant
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `restaurant` (
  `restaurant_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(90) NOT NULL,
  `location` VARCHAR(90) NOT NULL,
  `phone_number` VARCHAR(10) NOT NULL,
  `email` VARCHAR(90) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`restaurant_id`),
  INDEX `idx_name` (`name`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table: user
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `student_number` VARCHAR(45) NULL,
  `name` VARCHAR(45) NOT NULL,
  `surname` VARCHAR(45) NOT NULL,
  `date_of_birth` DATE NOT NULL,
  `cell_number` VARCHAR(45) NOT NULL,
  `email` VARCHAR(90) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE INDEX `idx_username` (`username`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table: menuItem
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `menuItem` (
  `menuItem_id` INT NOT NULL AUTO_INCREMENT,
  `sku` VARCHAR(45) NULL,
  `name` VARCHAR(90) NOT NULL,
  `description` VARCHAR(200) NOT NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `restaurant_id` INT NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`menuItem_id`),
  INDEX `fk_menuItem_restaurant_idx` (`restaurant_id`),
  CONSTRAINT `fk_menuItem_restaurant`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `restaurant` (`restaurant_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table: ingredient
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ingredient` (
  `ingredient_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(90) NOT NULL,
  `unit` ENUM('g', 'kg', 'ml', 'l', 'unit') NOT NULL,
  `amount` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`ingredient_id`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table: ingredient_per_menuItem
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `ingredient_per_menuItem` (
  `ingredient_per_menu_id` INT NOT NULL AUTO_INCREMENT,
  `menuItem_id` INT NOT NULL,
  `ingredient_id` INT NOT NULL,
  PRIMARY KEY (`ingredient_per_menu_id`),
  INDEX `fk_ingredient_menuItem_idx` (`menuItem_id`),
  INDEX `fk_ingredient_idx` (`ingredient_id`),
  CONSTRAINT `fk_ingredient_per_menuItem_menuItem`
    FOREIGN KEY (`menuItem_id`)
    REFERENCES `menuItem` (`menuItem_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_ingredient_per_menuItem_ingredient`
    FOREIGN KEY (`ingredient_id`)
    REFERENCES `ingredient` (`ingredient_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table: employee
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `employee` (
  `employee_id` INT NOT NULL AUTO_INCREMENT,
  `employee_name` VARCHAR(45) NOT NULL,
  `employee_surname` VARCHAR(45) NOT NULL,
  `restaurant_id` INT NOT NULL,
  `person_id` INT NOT NULL,
  `employee_username` VARCHAR(45) NOT NULL,
  `employee_password` VARCHAR(255) NOT NULL,
  `created_by` VARCHAR(45) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`employee_id`),
  UNIQUE INDEX `idx_employee_username` (`employee_username`),
  CONSTRAINT `fk_employee_person`
    FOREIGN KEY (`person_id`)
    REFERENCES `person` (`person_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_employee_restaurant`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `restaurant` (`restaurant_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table: orders
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `orders` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `order_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` ENUM('Submitted', 'Preparing', 'Ready', 'Completed', 'Declined') NOT NULL DEFAULT 'Submitted',
  `total_amount` DECIMAL(10,2) NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`order_id`),
  INDEX `fk_order_user_idx` (`user_id`),
  CONSTRAINT `fk_order_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`user_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table: orderItem
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `orderItem` (
  `orderItem_id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NOT NULL,
  `menuItem_id` INT NOT NULL,
  `restaurant_id` INT NOT NULL,
  PRIMARY KEY (`orderItem_id`),
  INDEX `fk_orderItem_order_idx` (`order_id`),
  INDEX `fk_orderItem_menuItem_idx` (`menuItem_id`),
  INDEX `fk_orderItem_restaurant_idx` (`restaurant_id`),
  CONSTRAINT `fk_orderItem_order`
    FOREIGN KEY (`order_id`)
    REFERENCES `orders` (`order_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_orderItem_menuItem`
    FOREIGN KEY (`menuItem_id`)
    REFERENCES `menuItem` (`menuItem_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_orderItem_restaurant`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `restaurant` (`restaurant_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table: restaurantUser
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `restaurantUser` (
  `restaurantUser_id` INT NOT NULL AUTO_INCREMENT,
  `restaurant_id` INT NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(255) NOT NULL,
  `user_type` ENUM('admin', 'POS') NOT NULL,
  `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`restaurantUser_id`),
  UNIQUE INDEX `idx_restaurant_username` (`username`),
  CONSTRAINT `fk_restaurantUser_restaurant`
    FOREIGN KEY (`restaurant_id`)
    REFERENCES `restaurant` (`restaurant_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Re-enable Checks
-- -----------------------------------------------------
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

