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
from src.category import Category
from src.interface import SelectionMenu
from src.api import Api
from src.util import string_to_list


class App():
    """
        Main application for Pur Beurre Substitute
    """

    def __init__(self):
        print('=== Bienvenue dans l\'application Pur Beurre Substitute ===')

        # Connect to the database
        self.database = Database(PBS_DB_NAME, PBS_USER, PBS_HOST, PBS_PASSWORD)
        self.database.connect_databse()

    @property
    def check_database(self):
        """
            Property for checking if the database is empty
        """
        return self.database.check_database()

    def first_start(self):
        """
            This method initialise the database if its empty
        """

        print('=> Première exécution de l\'application')

        # Initialize the API
        api = Api(API_URL_BASE, TMP_DIR)

        # Download data with the API
        api.download_products(API_CATEGORIES, API_PAGE_SIZE, API_PAGES)

        # Read data downloaded and clean uncompleted products
        api.read_json_with_key('products')
        api.clear_data(API_REQUIRED_KEYS)

        # Define each product as an object with variables attributes
        for product_data in api.data:
            categories = list()
            brands = list()
            stores = list()

            product = Product(**product_data)

            # Transform categories, brands and stores from a string to a list
            for data in string_to_list(product_data['categories']):
                categories.append(Category(data).name)
            if 'brands' in product_data:
                for data in string_to_list(product_data['brands']):
                    brands.append(Category(data).name)
            if 'stores' in product_data:
                for data in string_to_list(product_data['stores']):
                    stores.append(Category(data).name)

            # Add categories, stores and brands to the product
            product.add_categories(categories)
            product.add_stores(stores)
            product.add_brands(brands)

        # Insert products in the database
        progress_bar = FillingCirclesBar(f'Insertion des produits dans la base de données : ',
                                         max=len(Product.products))
        for product in Product.products:
            self.database.insert_product(product)
            progress_bar.next()
        progress_bar.finish()

        # Delete temporary files
        api.delete_files()

    def start_pur_beurre(self):
        """
            This method start the application
        """
        while True:
            # Get the user answer for the choosen category
            categories = SelectionMenu(*API_CATEGORIES)
            categories.display_choices('Choisissez une catégorie')
            categories.user_input('Sélectionnez une catégorie (numéro)')

            # Display available products in the chossen category
            query = ("""SELECT Products.name FROM Products
                     INNER JOIN Products_categories ON Products_categories.product_id = Products.id
                     INNER JOIN Categories ON Products_categories.category_id = Categories.id
                     WHERE Categories.name = %s
                     ORDER BY RAND() LIMIT 15""")
            result = self.database.select_in_database(query, (categories.choosen, ))
            choices = list()
            for (name,) in result:
                choices.append(name)

            # Get the user answer for the choosen product
            products = SelectionMenu(*choices)
            products.display_choices('Choisissez un produit')
            products.user_input('Sélectionnez un produit (numéro)')

            # Select the similar products in the database
            query = ("""SELECT DISTINCT Products.*,
                                        Categories.name,
                                        Brands.name,
                                        Stores.name
                     FROM Products
                     INNER JOIN Products_categories ON Products_categories.product_id = Products.id
                        INNER JOIN Categories ON Products_categories.category_id = Categories.id
                     INNER JOIN Products_stores ON Products_stores.product_id = Products.id
                        INNER JOIN Stores ON Products_stores.store_id = Stores.id
                     INNER JOIN Products_brands ON Products_brands.product_id = Products.id
                        INNER JOIN Brands ON Products_brands.brand_id = Brands.id
                     WHERE Categories.name = %s AND Products.name != %s""")
            result = self.database.select_in_database(query, (categories.choosen, products.choosen))

            # for product_data in result.fetchall():
            #     kwargs = {'code': product_data[1],
            #               'product_name': product_data[2],
            #               'generic_name_fr': product_data[3],
            #               'quantity': product_data[4],
            #               'ingredients_text': product_data[5],
            #               'nova_group': product_data[6],
            #               'nutriscore_grade': product_data[7],
            #               'url': product_data[8],
            #               'categories': product_data[9],
            #               'brands': product_data[10],
            #               'stores': product_data[11]}
            print(result.fetchall())
                # Product(**kwargs)
        self.database.close_database()


if __name__ == '__main__':

    pur_beurre = App() # pylint: disable=invalid-name

    # Check if database is not empty
    if pur_beurre.check_database is None:
        pur_beurre.first_start()
