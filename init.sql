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
    id INT UNSIGNED AUTO_INCREMENT,
    id_ext INT UNSIGNED NOT NULL,
    name VARCHAR(150) NOT NULL,
    common_name VARCHAR(150) NOT NULL,
    quantity VARCHAR(50),
    ingredients_list TEXT,
    nova_group CHAR(1),
    nutriscore_grade CHAR(1),
    url VARCHAR(250) NOT NULL,
    PRIMARY KEY(id)
) ENGINE = INNODB;

-- ---------------------------------------
-- CREATE A TABLE FOR Users
-- ---------------------------------------

CREATE TABLE Users (
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(150) NOT NULL,
    PRIMARY KEY(id)
) ENGINE = INNODB;

-- ---------------------------------------
-- CREATE A TABLE FOR Products_categories
-- ---------------------------------------

CREATE TABLE Products_categories (
    product_id INT UNSIGNED NOT NULL,
    category_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(product_id, category_id),
    CONSTRAINT fk_products_id_for_cat
        FOREIGN KEY (product_id)
        REFERENCES Products(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_categories_id
        FOREIGN KEY (category_id)
        REFERENCES Categories(id)
        ON DELETE CASCADE
) ENGINE = INNODB;

-- ---------------------------------------
-- CREATE A TABLE FOR Products_brands
-- ---------------------------------------

CREATE TABLE Products_brands (
    product_id INT UNSIGNED NOT NULL,
    brand_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(product_id, brand_id),
    CONSTRAINT fk_products_id_for_bra
        FOREIGN KEY (product_id)
        REFERENCES Products(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_brands_id
        FOREIGN KEY (brand_id)
        REFERENCES Brands(id)
        ON DELETE CASCADE
) ENGINE = INNODB;

-- ---------------------------------------
-- CREATE A TABLE FOR Products_stores
-- ---------------------------------------

CREATE TABLE Products_stores (
    product_id INT UNSIGNED NOT NULL,
    store_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(product_id, store_id),
    CONSTRAINT fk_products_id_for_sto
        FOREIGN KEY (product_id)
        REFERENCES Products(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_stores_id
        FOREIGN KEY (store_id)
        REFERENCES Stores(id)
        ON DELETE CASCADE
) ENGINE = INNODB;

-- ---------------------------------------
-- CREATE A TABLE FOR Products_traces
-- ---------------------------------------

CREATE TABLE Products_traces (
    product_id INT UNSIGNED NOT NULL,
    trace_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(product_id, trace_id),
    CONSTRAINT fk_products_id_for_tra
        FOREIGN KEY (product_id)
        REFERENCES Products(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_traces_id
        FOREIGN KEY (trace_id)
        REFERENCES Traces(id)
        ON DELETE CASCADE
) ENGINE = INNODB;

-- ---------------------------------------
-- CREATE A TABLE FOR Products_additives
-- ---------------------------------------

CREATE TABLE Products_additives (
    product_id INT UNSIGNED NOT NULL,
    additive_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(product_id, additive_id),
    CONSTRAINT fk_products_id_for_add
        FOREIGN KEY (product_id)
        REFERENCES Products(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_additives_id
        FOREIGN KEY (additive_id)
        REFERENCES Additives(id)
        ON DELETE CASCADE
) ENGINE = INNODB;

-- ---------------------------------------
-- CREATE A TABLE FOR Saved_products
-- ---------------------------------------

CREATE TABLE Saved_products (
    user_id INT UNSIGNED NOT NULL,
    product_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(user_id, product_id),
    CONSTRAINT fk_user_users_id
        FOREIGN KEY (user_id)
        REFERENCES Users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_product_products_id
        FOREIGN KEY (product_id)
        REFERENCES Products(id)
        ON DELETE CASCADE
) ENGINE = INNODB;