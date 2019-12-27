"""
    This module manage all operations with the database
"""
from collections import defaultdict

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

        # First insert categories
        query = ("INSERT INTO Categories (name) VALUES (%s)")
        for category in product.categories:
            values = (category,)
            self.insert_in_database(query, values)

        # Second insert brands
        query = ("INSERT INTO Brands (name) VALUES (%s)")
        for brand in product.brands:
            values = (brand,)
            self.insert_in_database(query, values)

        # Third insert stores
        query = ("INSERT INTO Stores (name) VALUES (%s)")
        for store in product.stores:
            values = (store,)
            self.insert_in_database(query, values)

        # Then insert the product
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

    def select_products(self, selected_category):
        """
            Method for selecting products based on a specific category
        """
        query = ("""SELECT Products.name, Products.code FROM Products
                 INNER JOIN Products_categories ON Products_categories.product_id = Products.id
                 INNER JOIN Categories ON Products_categories.category_id = Categories.id
                 WHERE Categories.name = %s
                 ORDER BY RAND() LIMIT 15""")
        result = self.select_in_database(query, (selected_category, ))
        available_products = list()
        for (name, code) in result:
            available_products.append({'name': name, 'code': code})

        return available_products

    def select_substitutes(self,
                           selected_category,
                           selected_product,
                           similar_categories,
                           substitutes_quantity):
        # pylint: disable=too-many-locals
        """
            Method for selecting all available subsitutes for a specific product
        """
        available_subs = list()

        # Select all products from "selected_category"
        query = ("""SELECT Products_categories.product_id,
                           Products_categories.category_id,
                           Products.code,
                           Products.name,
                           Products.nutriscore_grade
                 FROM Products_categories
                 INNER JOIN Products ON Products.id = Products_categories.product_id
                 WHERE Products_categories.product_id IN 
                 (SELECT product_id FROM Products_categories
                 INNER JOIN Products ON Products_categories.product_id = Products.id
                 INNER JOIN Categories ON Products_categories.category_id = Categories.id
                 WHERE Categories.name = %s AND Products.name != %s)""")
        query_values = (selected_category, selected_product['name'])

        subs = self.select_in_database(query, query_values)

        # Create a dict of products with a list of categories for each product
        # And the list of available products as substitutes
        subs_categories = defaultdict(list)
        for product in subs:
            subs_categories[product[0]].append(product[1])

            product = {'product_id': product[0],
                       'code': product[2],
                       'name': product[3],
                       'nutriscore_grade': product[4]}
            if product not in available_subs:
                available_subs.append(product)

        # Select categories for "selected_product"
        query = ("""SELECT Products_categories.product_id,
                           Products_categories.category_id,
                           Products.name,
                           Products.nutriscore_grade
                 FROM Products_categories
                 INNER JOIN Products ON Products.id = Products_categories.product_id
                 WHERE name = %s AND code = %s""")
        query_values = (selected_product['name'], selected_product['code'])

        orig_categories = self.select_in_database(query, query_values)
        orig_categories = [product[1] for product in orig_categories]

        orig_product = self.select_in_database(query, query_values).fetchone()
        orig_product = {'product_id': orig_product[0],
                        'name': orig_product[2],
                        'nutriscore_grade': orig_product[3]}

        # Count similar categories betwen the selected product and each substitutes products
        for product_id, product_categories in subs_categories.items():
            subs_categories[product_id] = set(orig_categories).intersection(product_categories)

            # We keep only the count of similar categories
            subs_categories[product_id] = len(subs_categories[product_id])

        # Add categories count to each product
        for i, product in enumerate(available_subs):
            product['categories_count'] = subs_categories[product['product_id']]
            available_subs[i] = product

        # Keep only substitutes if the count of common categories
        # is greater or equal to 'similar_categories'
        available_subs = [product\
                          for product in available_subs\
                          if product['categories_count'] >= similar_categories]

        # Keep only substitutes if the 'nutriscore_grade'
        # is less than original product's 'nutriscore_grade'
        available_subs = [product\
                          for product in available_subs\
                          if product['nutriscore_grade'] <= orig_product['nutriscore_grade']]

        # Sort by better 'nutriscore_grade' and greater 'similar_categories'
        available_subs.sort(key=lambda product: (product['nutriscore_grade'],
                                                 product['categories_count']))
        # The method return only
        available_subs = [{'name': product['name'], 'code': product['code']}\
                          for product in available_subs][:substitutes_quantity]

        return available_subs

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

    def close_database(self):
        """
            This method is called for closing the connection with the database
        """
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    print('Please don\'t load me alone...')
