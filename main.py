"""
    Main part for using Pur Beurre Substitute
    This application is made for the project 5 on OpenClassrooms during the Python courses
    The aim of this project is to use:
        - an API Rest,
        - a database like MySQL,
        - and of course Python.
"""
from progress.bar import FillingCirclesBar

from settings import * # pylint: disable=wildcard-import
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

        # Connect to the database
        self.database = Database(PBS_DB_NAME, PBS_USER, PBS_HOST, PBS_PASSWORD)
        self.database.connect_database()

        # Check if database is not empty
        if self.database.check_database() is None:
            self.first_start()

        continue_app = True
        while continue_app:
            if self.client() == 'Non':
                continue_app = False

        self.database.close_database()

    def first_start(self):
        """
            This method initialise the database if its empty
        """
        print('========== Première exécution de l\'application ===========')
        print('==> Téléchargement des données depuis Open Food Fact')

        # Initialize the API
        api = Api(API_URL_BASE, TMP_DIR)

        # Download data with the API
        api.download_products(API_CATEGORIES, API_PAGE_SIZE, API_PAGES)
        print('==> Téléchargement des données terminé !')

        # Read data downloaded and clean uncompleted products
        api.read_json_with_key('products')
        api.keep_required(API_DATA_FORMAT)
        api.format_data(API_DATA_FORMAT)

        # Define each product as an object with variables attributes
        for product_data in api.data:
            product = Product(**product_data)

        # Insert products in the database
        progress_bar = FillingCirclesBar(f'Insertion des produits dans la base de données : ',
                                         max=len(Product.products))
        for product in Product.products:
            self.database.insert_product(product)
            progress_bar.next()
        progress_bar.finish()

        # Delete temporary files
        api.delete_files()

        print('==> Fichiers temporaires supprimés')

    def client(self):
        """
            This method is the client for the application
        """
        categories = SelectionMenu(API_CATEGORIES)
        categories.display_choices('Choisissez une catégorie')
        categories.user_input('Sélectionnez une catégorie (numéro)')

        # Display available products in the chossen category
        available_products = self.database.select_products(categories.selected)

        # Get the user answer for the choosen product
        products = SelectionMenu(available_products)
        products.display_choices('Choisissez un produit')
        products.user_input('Sélectionnez un produit (numéro)')

        # Select in the database the substitutes to the selectd product
        available_substitutes = self.database.select_substitutes(categories.selected,
                                                                 products.selected,
                                                                 SIMILAR_CATEGORIES,
                                                                 SUBSTITUTE_QUANTITY)

        if available_substitutes:
            substitutes = SelectionMenu(available_substitutes)
            substitutes.display_choices('Choisissez un substitut')
            substitutes.user_input('Sélectionner un substitut (numéro)')
        else:
            print('\n')
            print('Nous n\'avons pas de substitut à vous proposer.')
            substitutes = None

        # Display the selected substitute
        if substitutes:
            product = Product(**self.database.select_product(substitutes.selected))
            product.display()
        else:
            product = None

        # Ask the user if she·he wants to save the product
        if product:
            register = SelectionMenu(['Oui', 'Non'])
            register.display_choices('Souhaitez-vous sauvegarder le produit ?')
            register.user_input('Sélectionnez une réponse (numéro)')

            if register.selected == 'Oui':
                self.database.save_product(product)

        # Ask the user if he wants to continue or end the application
        continue_app = SelectionMenu(['Oui', 'Non'])
        continue_app.display_choices('Souhaitez-vous continuez à utiliser l\'application ?')
        continue_app.user_input('Sélectionnez une réponse (numéro)')

        return continue_app.selected

if __name__ == '__main__':

    App()
