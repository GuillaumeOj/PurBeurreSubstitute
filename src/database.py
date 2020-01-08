"""
    This module manage all operations with the database
"""
import mysql.connector
from mysql.connector import errorcode


class Database:
    """
        This class manage differents operations with the database like:
            - connection
            - insert data
            - remove data
            - select data
    """

    def __init__(self, db_name, user, host, password):
        self.db_name = db_name
        self.user = user
        self.host = host
        self.password = password
        self.connection = False
        self.cursor = False

    def connect_database(self):
        """
            This method connect the application to the database
        """

        # Connect to the database
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                host=self.host,
                password=self.password,
                database=self.db_name)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception(f'Login informations are wrong. Please check "settings.py".\n{err}')
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception(f'The database does\'nt exist. Please check "settings.py".\n{err}')
            raise err
        else:
            self.cursor = self.connection.cursor(buffered=True)

    def check_database(self):
        """
            This method check if the database is empty
            If it is, run a method for filling it
        """
        try:
            query = 'SELECT * FROM Products LIMIT 1'
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            print(err)

        return self.cursor.fetchone()

    def check_users(self):
        """
            This method check if there is users in the database
        """
        query = "SELECT * FROM Users LIMIT 1"
        self.cursor.execute(query)

        return self.cursor.fetchone()

    def insert_in_database(self, query, values):
        """
            This method insert in the database with "query" as argument and an optionnal crieterion
            to manage possible duplicates entry
        """
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except mysql.connector.Error as err:
            if err.errno != 1062: # Duplicates entries
                print(err)

    def select_in_database(self, query, values=None):
        """
            This method select data in the database
        """
        try:
            self.cursor.execute(query, values)
        except mysql.connector.Error as err:
            print(err)

        return self.cursor

    def insert_product(self, product):
        """
            Insert a product in the database
        """

        # Insert the product
        query = ("""INSERT INTO Products
                 (code, name, common_name, quantity, ingredients_text, nutriscore_grade, url)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)""")
        values = (product.code,
                  product.name,
                  product.common_name,
                  product.quantity,
                  product.ingredients_text,
                  product.nutriscore_grade,
                  product.url)
        self.insert_in_database(query, values)

        # Insert categories
        query = ("INSERT INTO Categories (name) VALUES (%s)")
        for category in product.categories:
            values = (category,)
            self.insert_in_database(query, values)

        # Insert brands
        query = ("INSERT INTO Brands (name) VALUES (%s)")
        for brand in product.brands:
            values = (brand,)
            self.insert_in_database(query, values)

        # Insert stores
        query = ("INSERT INTO Stores (name) VALUES (%s)")
        for store in product.stores:
            values = (store,)
            self.insert_in_database(query, values)

        # Insert products categories
        query = ("""INSERT INTO Products_categories (product_id, category_id)
                 VALUES ((SELECT id FROM Products WHERE name=%s AND code=%s),
                 (SELECT id FROM Categories WHERE name=%s))""")
        for category in product.categories:
            values = (product.name, product.code, category)
            self.insert_in_database(query, values)

        # Insert products brands
        query = ("""INSERT INTO Products_brands (product_id, brand_id)
                 VALUES ((SELECT id FROM Products WHERE name=%s AND code=%s),
                 (SELECT id FROM Brands WHERE name=%s))""")
        for brand in product.brands:
            values = (product.name, product.code, brand)
            self.insert_in_database(query, values)

        # Insert products stores
        query = ("""INSERT INTO Products_stores (product_id, store_id)
                 VALUES ((SELECT id FROM Products WHERE name=%s AND code=%s),
                 (SELECT id FROM Stores WHERE name=%s))""")
        for store in product.stores:
            values = (product.name, product.code, store)
            self.insert_in_database(query, values)

    def select_products(self, selected_category, number_of_products, discriminant_criterion):
        """
            Method for selecting products based on a specific category
        """
        query = ("""SELECT
                        Products.name,
                        Products.code,
                        Products.nutriscore_grade 
                    FROM Products
                    INNER JOIN Products_categories ON Products_categories.product_id = Products.id
                    INNER JOIN Categories ON Products_categories.category_id = Categories.id
                    WHERE
                        Categories.name = %s
                        AND Products.nutriscore_grade > %s
                    ORDER BY RAND()
                    LIMIT %s
                """)
        values = (selected_category, discriminant_criterion, number_of_products)
        products = self.select_in_database(query, values)
        products = [{'name': product[0],
                     'code': product[1],
                     'nutriscore_grade': product[2]} for product in products]

        return products

    def select_substitutes(self,
                           selected_product,
                           number_of_similar_categories,
                           number_of_substitutes):
        """
            Method for selecting all available subsitutes for a specific product
        """
        query = ("""SELECT
                        Products_categories.product_id,
                        COUNT(Products_categories.product_id) AS common_categories,
                        Products.name,
                        Products.code,
                        Products.nutriscore_grade
                    FROM Products_categories
                    INNER JOIN Products ON Products.id = Products_categories.product_id
                    WHERE 
                        Products_categories.category_id IN (
                            SELECT Products_categories.category_id
                            FROM Products_categories
                            INNER JOIN Products ON Products_categories.product_id = Products.id
                            WHERE Products.code = %s)
                        AND Products.code != %s
                        AND Products.nutriscore_grade <= (
                            SELECT Products.nutriscore_grade
                            FROM Products
                            WHERE Products.code = %s)
                    GROUP BY Products_categories.product_id
                    HAVING common_categories >= %s
                    ORDER BY
                        Products.nutriscore_grade,
                        common_categories DESC
                    LIMIT %s;
                """)
        query_values = (selected_product['code'],
                        selected_product['code'],
                        selected_product['code'],
                        number_of_similar_categories,
                        number_of_substitutes)

        subsitutes = self.select_in_database(query, query_values)

        subsitutes = [{'name': product[2],
                       'code': product[3],
                       'nutriscore_grade': product[4]} for product in subsitutes]

        return subsitutes

    def select_product(self, selected_product):
        """
            Select all informations for a specific poduct based on his 'name'
        """
        # Select all informations in the products' table
        query = ("SELECT * FROM Products WHERE name = %s and code = %s")
        query_values = (selected_product['name'], selected_product['code'])

        product = self.select_in_database(query, query_values).fetchone()

        product = {'code': product[1],
                   'product_name': product[2],
                   'common_name': product[3],
                   'quantity': product[4],
                   'ingredients_text': product[5],
                   'nutriscore_grade': product[6],
                   'url': product[7]}

        # Select all categories for the product
        query = ("""SELECT Categories.name FROM Categories
                 INNER JOIN Products_categories ON Categories.id = Products_categories.category_id
                 INNER JOIN Products ON Products_categories.product_id = Products.id
                 WHERE Products.name = %s and Products.code = %s""")
        query_values = (selected_product['name'], selected_product['code'])

        categories = [category for (category, ) in self.select_in_database(query, query_values)]

        # Select all stores for the product
        query = ("""SELECT Stores.name FROM Stores
                 INNER JOIN Products_stores ON Stores.id = Products_stores.store_id
                 INNER JOIN Products ON Products_stores.product_id = Products.id
                 WHERE Products.name = %s and Products.code = %s""")
        query_values = (selected_product['name'], selected_product['code'])

        stores = [store for (store, ) in self.select_in_database(query, query_values)]

        # Select all brands for the product
        query = ("""SELECT Brands.name FROM Brands
                 INNER JOIN Products_brands ON Brands.id = Products_brands.brand_id
                 INNER JOIN Products ON Products_brands.product_id = Products.id
                 WHERE Products.name = %s and Products.code = %s""")
        query_values = (selected_product['name'], selected_product['code'])

        brands = [brand for (brand, ) in self.select_in_database(query, query_values)]

        product['categories'] = categories
        product['brands'] = brands
        product['stores'] = stores

        return product

    def save_product(self, product):
        """
            This method save a product as a favorites in the database
        """
        query = ("UPDATE Products SET saved = 1 WHERE name = %s AND code = %s")
        query_values = (product.name, product.code)

        self.insert_in_database(query, query_values)
        print('==> Produit enregistré')

    def select_saved_products(self):
        """
            Method for selecting saved products
        """
        query = ("SELECT Products.name, Products.code FROM Products WHERE Products.saved = 1")
        result = self.select_in_database(query)
        available_products = list()
        for (name, code) in result:
            available_products.append({'name': name, 'code': code})

        return available_products

    def close_database(self):
        """
            This method is called for closing the connection with the database
        """
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    print('Please don\'t load me alone...')
