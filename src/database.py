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

    def connect_databse(self):
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

    def close_database(self):
        """
            This method is called for closing the connection with the database
        """
        self.cursor.close()
        self.connection.close()

    def insert_product(self, product):
        """
            Insert a product in the database
        """

        # First insert categories
        query = ('INSERT INTO Categories'
                 '(name)'
                 'VALUES (%s)')
        for category in product.categories:
            values = (category,)
            self.insert_in_database(query, values)

        # Second insert brands
        query = ('INSERT INTO Brands'
                 '(name)'
                 'VALUES (%s)')
        for brand in product.brands:
            values = (brand,)
            self.insert_in_database(query, values)

        # Third insert stores
        query = ('INSERT INTO Stores'
                 '(name)'
                 'VALUES (%s)')
        for store in product.stores:
            values = (store,)
            self.insert_in_database(query, values)

        # Then insert the product
        query = ('INSERT INTO Products'
                 '(code, name, common_name, quantity, ingredients_text, nova_group,'
                 'nutriscore_grade, url)'
                 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)')
        values = (product.code,
                  product.name,
                  product.common_name,
                  product.quantity,
                  product.ingredients_text,
                  product.nova_group,
                  product.nutriscore_grade,
                  product.url)
        self.insert_in_database(query, values)

        # Insert products categories
        query = ('INSERT INTO Products_categories'
                 '(product_id, category_id)'
                 'VALUES'
                 '((SELECT id FROM Products WHERE name=%s AND code=%s),'
                 '(SELECT id FROM Categories WHERE name=%s))')
        for category in product.categories:
            values = (product.name, product.code, category)
            self.insert_in_database(query, values)

        # Insert products brands
        query = ('INSERT INTO Products_brands'
                 '(product_id, brand_id)'
                 'VALUES'
                 '((SELECT id FROM Products WHERE name=%s AND code=%s),'
                 '(SELECT id FROM Brands WHERE name=%s))')
        for brand in product.brands:
            values = (product.name, product.code, brand)
            self.insert_in_database(query, values)

        # Insert products stores
        query = ('INSERT INTO Products_stores'
                 '(product_id, store_id)'
                 'VALUES'
                 '((SELECT id FROM Products WHERE name=%s AND code=%s),'
                 '(SELECT id FROM Stores WHERE name=%s))')
        for store in product.stores:
            values = (product.name, product.code, store)
            self.insert_in_database(query, values)

    def select_products(self, selected_category):
        """
            Method for selecting products based on a specific category
        """
        query = ("""SELECT Products.name FROM Products
                 INNER JOIN Products_categories ON Products_categories.product_id = Products.id
                 INNER JOIN Categories ON Products_categories.category_id = Categories.id
                 WHERE Categories.name = %s
                 ORDER BY RAND() LIMIT 15""")
        result = self.select_in_database(query, (selected_category, ))
        available_products = list()
        for (name,) in result:
            available_products.append(name)

        return available_products


if __name__ == '__main__':
    print('Please don\'t load me alone...')
