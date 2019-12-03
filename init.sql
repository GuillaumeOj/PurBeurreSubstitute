DROP DATABASE IF EXISTS PBS;

CREATE DATABASE PBS CHARACTER SET 'utf8mb4';

USE PBS;

-- ---------------------------------------
-- CREATE A TABLE FOR Categories
-- ---------------------------------------

CREATE TABLE Categories (
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    url VARCHAR(250) NOT NULL,
    PRIMARY KEY(id)
);

-- ---------------------------------------
-- CREATE A TABLE FOR Brands
-- ---------------------------------------

CREATE TABLE Brands (
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    url VARCHAR(250) NOT NULL,
    PRIMARY KEY(id)
);

-- ---------------------------------------
-- CREATE A TABLE FOR Stores
-- ---------------------------------------

CREATE TABLE Stores (
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    url VARCHAR(250) NOT NULL,
    PRIMARY KEY(id)
) ENGINE = INNODB;

-- ---------------------------------------
-- CREATE A TABLE FOR Traces
-- ---------------------------------------

CREATE TABLE Traces (
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    url VARCHAR(250) NOT NULL,
    PRIMARY KEY(id)
) ENGINE = INNODB;

-- ---------------------------------------
-- CREATE A TABLE FOR Additives
-- ---------------------------------------

CREATE TABLE Additives (
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    url VARCHAR(250) NOT NULL,
    PRIMARY KEY(id)
) ENGINE = INNODB;

-- ---------------------------------------
-- CREATE A TABLE FOR Products
-- ---------------------------------------

CREATE TABLE Products (
    id INT UNSIGNED,
    name VARCHAR(150) NOT NULL,
    common_name VARCHAR(150) NOT NULL,
    quantity VARCHAR(50),
    ingredients_list TEXT,
    nova_group CHAR(1),
    nutriscore_grade CHAR(1),
    url VARCHAR(250) NOT NULL,
    PRIMARY KEY(id)
) ENGINE = INNODB;