"""
    Settings file for PurBeurreSubstitute
"""

# MySQL informations
PBS_DB_NAME = 'PBS'
PBS_USER = 'pbs'
PBS_HOST = 'localhost'
PBS_PASSWORD = 'pbs'
PBS_INIT_FILE = 'init.sql'

# Temp dir in which we download data
TMP_DIR = 'tmp/'

# Parameters for download data
API_PAGE_SIZE = 100
API_PAGES = 20
API_URL_BASE = 'https://fr.openfoodfacts.org/cgi/search.pl'
API_CATEGORIES = ['Aliments d\'origine végétale',
                  'Viandes',
                  'Boissons',
                  'Confiseries',
                  'Produits laitiers']
API_DATA_FORMAT = [{'name': 'product_name', 'type': str, 'length': 100, 'required': True},
                   {'name': 'generic_name_fr', 'type': str, 'length': 100, 'required': False},
                   {'name': 'categories', 'type': list, 'length': 100, 'required': True},
                   {'name': 'stores', 'type': list, 'length': 100, 'required': False},
                   {'name': 'brands', 'type': list, 'length': 100, 'required': False},
                   {'name': 'quantity', 'type': str, 'length': 50, 'required': False},
                   {'name': 'code', 'type': int, 'required': True},
                   {'name': 'nutriscore_grade', 'type': str, 'length': 1, 'required': True},
                   {'name': 'url', 'type': str, 'length': 250, 'required': True},
                   {'name': 'ingredients_text', 'type': str, 'required': False}]

NUMBER_OF_SIMILAR_CATEGORIES = 4
NUMBER_OF_PRODUCTS = 10
NUMBER_OF_SUBSTITUTES = 10
DISCRIMINANT_NUTRISCORE_GRADE = 'c'
