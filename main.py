"""
    Main part for using Pur Beurre Substitute
    This application is made for the project 5 on OpenClassrooms during the Python courses
    The aim of this project is to use:
        - an API Rest,
        - a database like MySQL,
        - and of course Python.
"""
from src.settings import * # pylint: disable=wildcard-import
from src.manage_database import ManageDatabase
from src.manage_api import ManageApi


def main():
    """
        Main function for running the application
    """

    # Connect to the database
    pbs_db = ManageDatabase(PBS_USER, PBS_HOST, PBS_PASSWORD)

    # Check if database is not empty
    if not pbs_db.check_database():
        manage_api = ManageApi(API_URL_BASE, TMP_DIR)
        manage_api.download_products(API_CATEGORIES, API_PAGE_SIZE, API_PAGES)
        manage_api.delete_files()


if __name__ == '__main__':
    main()
