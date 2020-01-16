"""
    This module manage all operations with the database
"""
import mysql.connector
from mysql.connector import errorcode


class Database:
    """
        This class manage differents operations with the database like:
            - connection
            - select a database
            - read an init file
            - check if the database is not empty
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
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                host=self.host,
                password=self.password)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message = f'Les informations de connexion sont eronnées.'
                message = f'{message} Merci de vérifier "settings.py"'
                message = f'{message} ou de suivre les instructions du Readme.md.\n{err}'
                raise Exception(message)
            raise err

        self.cursor = self.connection.cursor(buffered=True)

    def select_database(self):
        """
            This method select the database
        """
        try:
            self.connection.database = self.db_name
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                message = f'La base de données n\'existe pas.'
                message = f'{message} Merci de vérifier "settings.py"'
                message = f'{message} ou de suivre les instructions de démarrage.\n{err}'
                raise Exception(message)
            raise err

    def read_init_file(self, init_file):
        """
            This method read an sql file and execute each commands
        """
        with open(init_file, 'r') as sql_file:
            # Read all the file as a string
            sql_commands = sql_file.read()

            # Split the file in a list by using ';' as a separator for each SQL command
            sql_commands = sql_commands.split(';')

        # Eaxecute each command
        for command in sql_commands:
            self.cursor.execute(command)

    def check_database(self):
        """
            This method check if there is products in the database
        """
        try:
            query = 'SELECT * FROM Products LIMIT 1'
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_NO_SUCH_TABLE:
                message = f'La base de données ne contient aucune table.'
                message = f'{message} Merci de lancer le script avec l\'option --init.\n{err}'
                raise Exception(message)
            raise err

        return self.cursor.fetchone()

    def insert_in_database(self, query, values):
        """
            This method insert data in the database
        """
        try:
            if isinstance(values, tuple):
                self.cursor.execute(query, values)
            else:
                self.cursor.executemany(query, values)
            self.connection.commit()
        except mysql.connector.Error as err:
            raise err

    def select_in_database(self, query, values=None):
        """
            This method select data in the database
        """
        try:
            self.cursor.execute(query, values)
        except mysql.connector.Error as err:
            raise err

        return self.cursor

    def insert_products(self, products):
        """
            Insert a product in the database
        """
        print('Insertion des produits...')
        query = ("""INSERT IGNORE INTO Products
                    (code, name, common_name, quantity, ingredients_text, nutriscore_grade, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                 """)
        values = [(product.code,
                   product.name,
                   product.common_name,
                   product.quantity,
                   product.ingredients_text,
                   product.nutriscore_grade,
                   product.url) for product in products]
        self.insert_in_database(query, values)

        print('Insertion des catégories...')
        # Insert categories
        query = ("INSERT IGNORE INTO Categories (name) VALUES (%s)")
        values = [(category,) for product in products for category in product.categories]
        self.insert_in_database(query, values)

        print('Insertion des marques...')
        # Insert brands
        query = ("INSERT IGNORE INTO Brands (name) VALUES (%s)")
        values = [(brand,) for product in products for brand in product.brands]
        self.insert_in_database(query, values)

        print('Insertion des magasins...')
        # Insert stores
        query = ("INSERT IGNORE INTO Stores (name) VALUES (%s)")
        values = [(store,) for product in products for store in product.stores]
        self.insert_in_database(query, values)

        print('Association des produits et des catégories...')
        # Insert products categories
        query = ("""INSERT IGNORE INTO Products_categories (product_id, category_id)
                    VALUES (
                        (SELECT id FROM Products WHERE code=%s),
                        (SELECT id FROM Categories WHERE name=%s)
                    )
                 """)
        values = [(product.code,
                   category) for product in products for category in product.categories]
        self.insert_in_database(query, values)

        print('Association des produits et des marques...')
        # Insert products brands
        query = ("""INSERT IGNORE INTO Products_brands (product_id, brand_id)
                    VALUES (
                        (SELECT id FROM Products WHERE code=%s),
                        (SELECT id FROM Brands WHERE name=%s)
                    )
                 """)
        values = [(product.code, brand) for product in products for brand in product.brands]
        self.insert_in_database(query, values)

        print('Association des produits et des magasins...')
        # Insert products stores
        query = ("""INSERT IGNORE INTO Products_stores (product_id, store_id)
                    VALUES (
                        (SELECT id FROM Products WHERE code=%s),
                        (SELECT id FROM Stores WHERE name=%s)
                    )
                 """)
        values = [(product.code, store) for product in products for store in product.stores]
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
            Method for select all available subsitutes for the selected product
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
                    LIMIT %s
                """)
        query_values = (selected_product.code,
                        selected_product.code,
                        selected_product.code,
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
        query = ("""SELECT
                        Products.code,
                        Products.name,
                        Products.common_name,
                        Products.quantity,
                        Products.ingredients_text,
                        Products.nutriscore_grade,
                        Products.url,
                        Categories.name AS categories_name,
                        Stores.name AS stores_name,
                        Brands.name AS brands_name
                    FROM Products
                    LEFT JOIN Products_categories
                        ON Products_categories.product_id = Products.id
                    LEFT JOIN Categories
                        ON Categories.id = Products_categories.category_id
                    LEFT JOIN Products_stores
                        ON Products_stores.product_id = Products.id
                    LEFT JOIN Stores
                        ON Stores.id = Products_stores.store_id
                    LEFT JOIN Products_brands
                        ON Products_brands.product_id = Products.id
                    LEFT JOIN Brands
                        ON Brands.id = Products_brands.brand_id
                    WHERE Products.code = %s
                 """)
        query_values = (selected_product['code'],)

        product_rows = self.select_in_database(query, query_values)

        product = dict()
        categories = list()
        stores = list()
        brands = list()

        # Create a dict for the product
        for row in product_rows:
            if not product:
                product = {'code': row[0],
                           'product_name': row[1],
                           'common_name': row[2],
                           'quantity': row[3],
                           'ingredients_text': row[4],
                           'nutriscore_grade': row[5],
                           'url': row[6]}
            category = row[7]
            store = row[8]
            brand = row[9]

            if category not in categories:
                categories.append(category)
            if store and store not in stores:
                stores.append(store)
            if brand and brand not in brands:
                brands.append(brand)

        # Add categories, stores and brands to the prodcut's dict
        product['categories'] = categories
        product['stores'] = stores
        product['brands'] = brands

        return product

    def save_product(self, to_substitute, substituted):
        """
            This method save a product in the database
        """
        query = ("""INSERT INTO Saved_products
                    (to_substitute_id, substituted_id)
                    VALUES (
                        (SELECT Products.id FROM Products WHERE Products.code = %s),
                        (SELECT Products.id FROM Products WHERE Products.code = %s)
                    )
                 """)
        query_values = (to_substitute.code, substituted.code)

        self.insert_in_database(query, query_values)
        print('==> Produit enregistré')

    def select_saved_products(self):
        """
            Method for selecting saved products
        """
        query = ("""SELECT
                        'to_substitute',
                        Saved_products.to_substitute_id,
                        Products.name,
                        Products.nutriscore_grade,
                        Products.code
                    FROM Products
                    INNER JOIN Saved_products ON Saved_products.to_substitute_id = Products.id
                    UNION ALL
                    SELECT
                        'substituted',
                        Saved_products.substituted_id,
                        Products.name,
                        Products.nutriscore_grade,
                        Products.code
                    FROM Products
                    INNER JOIN Saved_products ON Saved_products.substituted_id = Products.id
                 """)
        result = self.select_in_database(query)

        to_substitute_products = list()
        substituted_products = list()

        for row in result:
            name = row[2]
            nutriscore_grade = row[3]
            code = row[4]

            # Make the difference between the product to substitute
            # and the product used as a substitute
            if row[0] == 'to_substitute':
                to_substitute_products.append({'name': name,
                                               'nutriscore_grade': nutriscore_grade,
                                               'code': code})
            else:
                substituted_products.append({'name': name,
                                             'nutriscore_grade': nutriscore_grade,
                                             'code': code})

        return (to_substitute_products, substituted_products)

    def close_database(self):
        """
            Method for closing the connection with the database
        """
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    print('Please don\'t load me alone...')
