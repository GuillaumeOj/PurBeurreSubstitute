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
from src.util import clear_data
from src.product import Product


def main():
    """
        Main function for running the application
    """

    # Connect to the database
    pbs_db = Database(PBS_DB_NAME, PBS_USER, PBS_HOST, PBS_PASSWORD)

    # Check if database is not empty
    if pbs_db.connect_databse() and not pbs_db.check_database():
        # Initialize the API
        api = Api(API_URL_BASE, TMP_DIR)
        # Download data with the API
        api.download_products(API_CATEGORIES, API_PAGE_SIZE, API_PAGES)

        # Read data downloaded
        products_list = api.read_json_with_key('products')

        # Filter data by deleting products without required keys and values
        products_list = clear_data(products_list, *REQUIRED_KEYS, **REQUIRED_VALUES)

        # Define each product as an object with variables attributes
        for line in products_list:
            Product(**line)

        # Insert products in the database
        for product in Product.products:
            # First insert categories
            query = ('INSERT INTO Categories'
                     '(name)'
                     'VALUES (%s)')
            product.categories = product.attribute_to_list('categories')
            for element in product.categories:
                pbs_db.insert_in_database(query, element)

            # Second insert brands
            query = ('INSERT INTO Brands'
                     '(name)'
                     'VALUES (%s)')
            product.brands = product.attribute_to_list('brands')
            for element in product.brands:
                pbs_db.insert_in_database(query, element)

            # Third insert stores
            if hasattr(product, 'stores'):
                query = ('INSERT INTO Stores'
                         '(name)'
                         'VALUES (%s)')
                product.stores = product.attribute_to_list('stores')
                for element in product.stores:
                    pbs_db.insert_in_database(query, element)

            # Then insert the product
            query = ('INSERT INTO Products'
                     '(id_ext, name, common_name, quantity, ingredients_list, nova_group,'
                     'nutriscore_grade, url)'
                     'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)')
            values = product.attributes_to_tuple(PRODUCT_ATTR_ORDER, PRODUCT_ATTR_TYPE)
            pbs_db.insert_in_database(query, values)

        # Delete temporary files
        api.delete_files()


if __name__ == '__main__':
    main()
