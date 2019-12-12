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


def main():
    """
        Main function for running the application
    """

    # Connect to the database
    pbs_db = Database(PBS_USER, PBS_HOST, PBS_PASSWORD)

    # Check if database is not empty
    if not pbs_db.check_database():
        # Initialize the API
        api = Api(API_URL_BASE, TMP_DIR)
        # Download data with the API
        api.download_products(API_CATEGORIES, API_PAGE_SIZE, API_PAGES)

        # Read data downloaded
        products_list = api.read_json_with_key('products')

        # Filter data by deleting products without required keys and values
        products_list = clear_data(products_list, *REQUIRED_KEYS, **REQUIRED_VALUES)

        # Delete temporary files
        api.delete_files()


if __name__ == '__main__':
    main()
