"""
    Main part for using Pur Beurre Substitute
    This application is made for the project 5 on OpenClassrooms during the Python courses
    The aim of this project is to use:
        - an API Rest,
        - a database like MySQL,
        - and of course Python.
"""
from init import init_pur_beurre
from settings import PBS_DB_NAME, PBS_USER, PBS_HOST, PBS_PASSWORD
from src.database import Database
# from src.product import Product
from src.interface import SelectionMenu


def main():
    """
        Main function for running the application
    """
    print('=== Bienvenue dans l\'applcation Pur Beurre Substitute ===')

    # Connect to the database
    pbs_db = Database(PBS_DB_NAME, PBS_USER, PBS_HOST, PBS_PASSWORD)
    pbs_db.connect_databse()

    # Check if database is not empty
    if pbs_db.check_database() is None:
        init_pur_beurre(pbs_db)

    # Here start the application
    while True:
        # Display available categories
        query = ('SELECT name FROM Categories ORDER BY RAND() LIMIT 10')
        result = pbs_db.select_in_database(query)
        choices = list()
        for (name,) in result:
            choices.append(name)

        # Get the user answer for the choosen category
        categories = SelectionMenu(*choices)
        categories.display_choices('Choisissez une catégorie')
        categories.user_input('Sélectionnez une catégorie (numéro)')

        # Display available products in the chossen category
        query = ("""SELECT Products.name FROM Products
                 INNER JOIN Products_categories ON Products_categories.product_id = Products.id
                 INNER JOIN Categories ON Products_categories.category_id = Categories.id
                 WHERE Categories.name = %s
                 ORDER BY RAND() LIMIT 15""")
        result = pbs_db.select_in_database(query, (categories.choosen, ))
        choices = list()
        for (name,) in result:
            choices.append(name)

        # Get the user answer for the choosen product
        products = SelectionMenu(*choices)
        products.display_choices('Choisissez un produit')
        products.user_input('Sélectionnez un produit (numéro)')

        # Select the similar products in the database
        query = ("""SELECT Products.*,
                           Categories.name AS categories_name,
                           Brands.name AS brands_name,
                           Stores.name AS stores_name
                 FROM Products
                 INNER JOIN Products_categories ON Products_categories.product_id = Products.id
                    INNER JOIN Categories ON Products_categories.category_id = Categories.id
                 INNER JOIN Products_stores ON Products_stores.product_id = Products.id
                    INNER JOIN Stores ON Products_stores.store_id = Stores.id
                 INNER JOIN Products_brands ON Products_brands.product_id = Products.id
                    INNER JOIN Brands ON Products_brands.brand_id = Brands.id
                 WHERE Categories.name = %s AND Products.name != %s""")
        result = pbs_db.select_in_database(query, (categories.choosen, products.choosen))

        print(type(result))
        break
    pbs_db.close_database()


if __name__ == '__main__':
    main()
