"""
    Main part for using Pur Beurre Substitute
    This application is made for the project 5 on OpenClassrooms during the Python courses
    The aim of this project is to use:
        - an API Rest,
        - a database like MySQL,
        - and of course Python.
"""
from settings import * # pylint: disable=wildcard-import
from src.database import Database
from src.api import Api
from src.product import Product


def main():
    """
        Main function for running the application
    """

    # Connect to the database
    pbs_db = Database(PBS_DB_NAME, PBS_USER, PBS_HOST, PBS_PASSWORD)
    pbs_db.connect_databse()

    # Check if database is not empty
    if pbs_db.check_database() is None:
        # Initialize the API
        api = Api(API_URL_BASE, TMP_DIR)
        # Download data with the API
        api.download_products(API_CATEGORIES, API_PAGE_SIZE, API_PAGES)

        # Read data downloaded
        api.read_json_with_key('products')

        # Define each product as an object with variables attributes
        for line in api.data:
            Product(**line)

        # Insert products in the database
        for product in Product.products:

            required_attributes = [product.categories,
                                   product.brands,
                                   product.stores,
                                   product.id_ext,
                                   product.name,
                                   product.nova,
                                   product.nutriscore,
                                   product.url]
            if all(attribute is not None for attribute in required_attributes):
                # First insert categories
                query = ('INSERT INTO Categories'
                         '(name)'
                         'VALUES (%s)')
                for category in product.categories:
                    values = (category,)
                    pbs_db.insert_in_database(query, values)

                # Second insert brands
                query = ('INSERT INTO Brands'
                         '(name)'
                         'VALUES (%s)')
                for brand in product.brands:
                    values = (brand,)
                    pbs_db.insert_in_database(query, values)

                # Third insert stores
                query = ('INSERT INTO Stores'
                         '(name)'
                         'VALUES (%s)')
                for store in product.stores:
                    values = (store,)
                    pbs_db.insert_in_database(query, values)

                # Then insert the product
                query = ('INSERT INTO Products'
                         '(id_ext, name, common_name, quantity, ingredients_list, nova_group,'
                         'nutriscore_grade, url)'
                         'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)')
                values = (product.id_ext,
                          product.name,
                          product.common_name,
                          product.quantity,
                          product.ingredients,
                          product.nova,
                          product.nutriscore,
                          product.url)
                pbs_db.insert_in_database(query, values)

                # Insert products categories
                query = ('INSERT INTO Products_categories'
                         '(product_id, category_id)'
                         'VALUES'
                         '((SELECT id FROM Products WHERE name=%s),'
                         '(SELECT id FROM Categories WHERE name=%s))')
                for category in product.categories:
                    values = (product.name, category)
                    pbs_db.insert_in_database(query, values)

                # Insert products brands
                query = ('INSERT INTO Products_brands'
                         '(product_id, brand_id)'
                         'VALUES'
                         '((SELECT id FROM Products WHERE name=%s),'
                         '(SELECT id FROM Brands WHERE name=%s))')
                for brand in product.brands:
                    values = (product.name, brand)
                    pbs_db.insert_in_database(query, values)

                # Insert products stores
                query = ('INSERT INTO Products_stores'
                         '(product_id, store_id)'
                         'VALUES'
                         '((SELECT id FROM Products WHERE name=%s),'
                         '(SELECT id FROM Stores WHERE name=%s))')
                for store in product.stores:
                    values = (product.name, store)
                    pbs_db.insert_in_database(query, values)

        # Delete temporary files
        api.delete_files()
    pbs_db.close_database()


if __name__ == '__main__':
    main()
