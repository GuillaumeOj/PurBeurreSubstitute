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
);

-- ---------------------------------------
-- CREATE A TABLE FOR Traces
-- ---------------------------------------

CREATE TABLE Traces (
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    url VARCHAR(250) NOT NULL,
    PRIMARY KEY(id)
);