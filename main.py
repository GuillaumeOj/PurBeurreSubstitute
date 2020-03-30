"""
    Application using Pur Beurre Substitute
    This application is made for the project 5 on OpenClassrooms during the
    Python courses
    The aim of this project is to use:
        - an API Rest,
        - a database like MySQL,
        - and of course Python.
"""
import argparse

from settings import PBS_DB_NAME, PBS_HOST, PBS_USER, PBS_PASSWORD
from settings import PBS_INIT_FILE
from settings import API_PAGES, API_PAGE_SIZE, API_CATEGORIES, API_URL_BASE
from settings import API_DATA_FORMAT
from settings import NUMBER_OF_PRODUCTS, NUMBER_OF_SIMILAR_CATEGORIES
from settings import DISCRIMINANT_NUTRISCORE_GRADE, NUMBER_OF_SUBSTITUTES
from settings import TMP_DIR
from src.database import Database
from src.product import Product
from src.interface import SelectionMenu
from src.api import Api


class App():
    """
        Main application for Pur Beurre Substitute
    """

    def __init__(self):
        print('=== Bienvenue dans l\'application Pur Beurre Substitute ===')

        # Add an argument for initialise the database
        parser = argparse.ArgumentParser()
        parser.add_argument('-i',
                            '--initdb',
                            help='Initialize the database',
                            action='store_true')
        arguments = parser.parse_args()

        # Connect to the database
        self.database = Database(PBS_DB_NAME, PBS_USER, PBS_HOST, PBS_PASSWORD)
        self.database.connect_database()

        # If the user use 'initdb' as argument, call a method in Database
        # for reading the 'init.sql' file
        if arguments.initdb:
            # Confirmation message for safety and avoid 'initdb' by mistake
            menu_title = 'Êtes-vous sûr de vouloir réinitialiser la base de'
            menu_title += ' données ?'
            answers_title = 'Sélectionnez une réponse (numéro)'
            answers = ['Oui', 'Non']

            initialize = SelectionMenu(menu_title, answers_title, answers)

            if initialize.selected == 'Oui':
                self.database.read_init_file(PBS_INIT_FILE)

        # Select the database
        self.database.select_database()

        # Check if database is not empty
        if self.database.check_database() is None:
            self.first_start()

        while True:
            # Ask the user if he wants:
            # - Find a substitute for a product
            # - Read a substitute already save in the database
            menu_title = 'Que souhaitez-vous faire'
            answers_title = 'Sélectionnez une option (numéro)'
            answers = ['Substituer un aliment',
                       'Retrouver un aliment déjà substitué']

            app_usage = SelectionMenu(menu_title, answers_title, answers)

            if app_usage.selected == 'Substituer un aliment':
                self.find_substitute()
            else:
                self.find_saved()

            # Ask the user if he wants to continue or end the application
            menu_title = 'Souhaitez-vous continuer à utiliser l\'application ?'
            answers_title = 'Sélectionnez une réponse (numéro)'
            answers = ['Oui', 'Non']

            continue_app = SelectionMenu(menu_title, answers_title, answers)

            if continue_app.selected == 'Non':
                break

        self.database.close_database()

    def first_start(self):
        """
            This method initialise the database if its empty
        """
        print('')
        print('========== Première exécution de l\'application ===========')
        print('==> Téléchargement des données depuis l\'Open Food Facts')

        # Initialize the API
        api = Api(API_URL_BASE, TMP_DIR)

        # Download data with the API
        api.download_products(API_CATEGORIES, API_PAGE_SIZE, API_PAGES)
        print('')
        print('==> Téléchargement des données terminé !')

        # Read data downloaded and clean uncompleted products
        api.read_json_with_key('products')
        api.keep_required(API_DATA_FORMAT)
        api.format_data(API_DATA_FORMAT)

        # Define each product as an object with variables attributes
        for product_data in api.data:
            product = Product(**product_data)

        # Insert products in the database
        self.database.insert_products(product.products)

        # Delete temporary files
        api.delete_files()

    def find_substitute(self):
        """
            This method is the client for the application
        """
        # Ask the user to choose a category
        menu_title = 'Choisissez une catégorie'
        answers_title = 'Sélectionnez une catégorie (numéro)'
        answers = API_CATEGORIES

        category = SelectionMenu(menu_title, answers_title, answers)

        # Ask user to choose a product to substitute
        to_substitute = None

        while not to_substitute:
            # Display available products in the chossen category
            available_products = self.database.select_products(
                category.selected,
                NUMBER_OF_PRODUCTS,
                DISCRIMINANT_NUTRISCORE_GRADE)
            available_products.append('Afficher d\'autres produits au hasard')
            menu_title = 'Choisissez un produit à subsituer'
            answers_title = 'Sélectionnez un produit (numéro)'
            answers = available_products

            product = SelectionMenu(menu_title, answers_title, answers)

            if product.selected != 'Afficher d\'autres produits au hasard':
                to_substitute = Product(
                    **self.database.select_product(product.selected))

        # Select in the database the potential substitutes for to the selected
        # product
        available_substitutes = self.database.select_substitutes(
            to_substitute, NUMBER_OF_SIMILAR_CATEGORIES, NUMBER_OF_SUBSTITUTES)

        if available_substitutes:
            # Ask the user to choose a substitute
            menu_title = 'Choisissez un substitut'
            answers_title = 'Sélectionner un substitut (numéro)'
            answers = available_substitutes

            substitute = SelectionMenu(menu_title, answers_title, answers)

            substituted = Product(
                **self.database.select_product(substitute.selected))
            substituted.display()
        else:
            print('Nous n\'avons pas de substitut à vous proposer.')
            substituted = None

        if substituted:
            # Ask the user if she·he wants to save the product
            menu_title = 'Souhaitez-vous sauvegarder le produit ?'
            answers_title = 'Sélectionnez une réponse (numéro)'
            answers = ['Oui', 'Non']

            save = SelectionMenu(menu_title, answers_title, answers)

            if save.selected == 'Oui':
                self.database.save_product(to_substitute, substituted)

    def find_saved(self):
        """
            This method display the products already saved by the user
        """
        # Get all products saved in the database
        saved_products = self.database.select_saved_products()

        if saved_products:
            # Ask the user which product she·he wants to read
            menu_title = 'Quel substitut souhaitez-vous consulter ?'
            answers_title = 'Sélectionnez le substitut (numéro)'
            answers = saved_products

            substituted = SelectionMenu(menu_title, answers_title, answers)
        else:
            print('Aucun substitut n\'a était sauvegardé pour l\'instant')
            substituted = None

        if substituted:
            # Display the selected subsitute
            product = Product(
                **self.database.select_product(substituted.selected))
            product.display()


if __name__ == '__main__':
    App()
