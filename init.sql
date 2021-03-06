DROP DATABASE IF EXISTS PBS;

CREATE DATABASE PBS CHARACTER SET 'utf8mb4';

USE PBS;

-- ---------------------------------------
-- CREATE A TABLE FOR Categories
-- ---------------------------------------

CREATE TABLE Categories (
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY(id),
    UNIQUE INDEX ind_cat_name(name)
);

-- ---------------------------------------
-- CREATE A TABLE FOR Brands
-- ---------------------------------------

CREATE TABLE Brands (
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY(id),
    UNIQUE INDEX ind_brand_name(name)

);

-- ---------------------------------------
-- CREATE A TABLE FOR Stores
-- ---------------------------------------

CREATE TABLE Stores (
    id INT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    PRIMARY KEY(id),
    UNIQUE INDEX ind_store_name(name)
) ENGINE = INNODB;

-- ---------------------------------------
-- CREATE A TABLE FOR Products
-- ---------------------------------------

CREATE TABLE Products (
    id INT UNSIGNED AUTO_INCREMENT,
    code BIGINT UNSIGNED NOT NULL,
    name VARCHAR(100) NOT NULL,
    common_name VARCHAR(100),
    quantity VARCHAR(50),
    ingredients_text TEXT,
    nutriscore_grade CHAR(1) NOT NULL,
    url VARCHAR(250) NOT NULL,
    PRIMARY KEY(id),
    UNIQUE INDEX ind_code_name(code, name)
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
-- CREATE A TABLE FOR Saved_products
-- ---------------------------------------

CREATE TABLE Saved_products (
    to_substitute_id INT UNSIGNED NOT NULL,
    substituted_id INT UNSIGNED NOT NULL,
    PRIMARY KEY(to_substitute_id, substituted_id),
    CONSTRAINT fk_to_substitute_id
        FOREIGN KEY (to_substitute_id)
        REFERENCES Products(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_substituted_id
        FOREIGN KEY (substituted_id)
        REFERENCES Products(id)
        ON DELETE CASCADE
) ENGINE = INNODB;