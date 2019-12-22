"""
    This module define a product and all method associated
"""


class Product: # pylint: disable=too-many-instance-attributes
    """
        This class allow to create a structred object with many arguments
    """

    products = list()

    def __init__(self, **kwargs):

        self.categories = None
        self.brands = None
        self.stores = None

        self.code = int(kwargs['code'])
        self.name = kwargs['product_name'][:200]
        self.nova_group = int(kwargs['nova_group'])
        self.nutriscore_grade = kwargs['nutriscore_grade'][:1]
        self.url = kwargs['url'][:250]

        self.common_name = str()
        self.quantity = str()
        self.ingredients_text = str()

        if 'generic_name_fr' in kwargs:
            self.common_name = kwargs['generic_name_fr'][:200]
        if 'quantity' in kwargs:
            self.quantity = kwargs['quantity'][:50]
        if 'ingredients_text' in kwargs:
            self.ingredients_text = kwargs['ingredients_text']

        Product.products.append(self)

    @property
    def count(self):
        """
            Give the number of products
        """
        print(len(Product.products))
        return len(Product.products)

    def add_categories(self, categories):
        """
            Associate multiple categories to this product
        """
        self.categories = categories

    def add_stores(self, stores):
        """
            Associate multiple stores to this product
        """
        self.stores = stores

    def add_brands(self, brands):
        """
            Associate multiple brands to this product
        """
        self.brands = brands

    def insert_product(self, database):
        """
            Insert the product in the database
        """

        # First insert categories
        query = ('INSERT INTO Categories'
                 '(name)'
                 'VALUES (%s)')
        for category in self.categories:
            values = (category,)
            database.insert_in_database(query, values)

        # Second insert brands
        query = ('INSERT INTO Brands'
                 '(name)'
                 'VALUES (%s)')
        for brand in self.brands:
            values = (brand,)
            database.insert_in_database(query, values)

        # Third insert stores
        query = ('INSERT INTO Stores'
                 '(name)'
                 'VALUES (%s)')
        for store in self.stores:
            values = (store,)
            database.insert_in_database(query, values)

        # Then insert the product
        query = ('INSERT INTO Products'
                 '(code, name, common_name, quantity, ingredients_text, nova_group,'
                 'nutriscore_grade, url)'
                 'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)')
        values = (self.code,
                  self.name,
                  self.common_name,
                  self.quantity,
                  self.ingredients_text,
                  self.nova_group,
                  self.nutriscore_grade,
                  self.url)
        database.insert_in_database(query, values)

        # Insert products categories
        query = ('INSERT INTO Products_categories'
                 '(product_id, category_id)'
                 'VALUES'
                 '((SELECT id FROM Products WHERE name=%s AND code=%s),'
                 '(SELECT id FROM Categories WHERE name=%s))')
        for category in self.categories:
            values = (self.name, self.code, category)
            database.insert_in_database(query, values)

        # Insert products brands
        query = ('INSERT INTO Products_brands'
                 '(product_id, brand_id)'
                 'VALUES'
                 '((SELECT id FROM Products WHERE name=%s AND code=%s),'
                 '(SELECT id FROM Brands WHERE name=%s))')
        for brand in self.brands:
            values = (self.name, self.code, brand)
            database.insert_in_database(query, values)

        # Insert products stores
        query = ('INSERT INTO Products_stores'
                 '(product_id, store_id)'
                 'VALUES'
                 '((SELECT id FROM Products WHERE name=%s AND code=%s),'
                 '(SELECT id FROM Stores WHERE name=%s))')
        for store in self.stores:
            values = (self.name, self.code, store)
            database.insert_in_database(query, values)



if __name__ == '__main__':
    print('Please don\'t load me alone...')
