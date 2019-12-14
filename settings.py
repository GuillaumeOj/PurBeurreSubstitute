"""
    Settings file for PurBeurreSubstitute
"""

# MySQL informations
PBS_DB_NAME = 'PBS'
PBS_USER = 'pbs'
PBS_HOST = 'localhost'
PBS_PASSWORD = 'pbs'

# Temp dir in which we download data
TMP_DIR = 'tmp/'

# Parameters for download data
API_PAGE_SIZE = 20
API_PAGES = 1
API_URL_BASE = 'https://fr.openfoodfacts.org/cgi/search.pl'
API_CATEGORIES = ['aliments-d-origine-vegetale',
                  'viandes',
                  'boissons',
                  'confiseries',
                  'produits-laitiers']

# Required keys for each products
REQUIRED_KEYS = ['product_name',
                 'code',
                 'nutriscore_grade',
                 'nova_group',
                 'url',
                 'categories_lc']
REQUIRED_VALUES = {'categories_lc': 'fr'}

# Attributes for insert a product in the database
PRODUCT_ATTR_ORDER = {'1': 'product_name',
                      '0': 'code',
                      '6': 'nutriscore_grade',
                      '5': 'nova_group',
                      '7': 'url',
                      '2': 'generic_name_fr',
                      '3': 'quantity',
                      '4': 'ingredients_text'}
PRODUCT_ATTR_TYPE = {'product_name': 'str',
                     'code': 'int',
                     'nutriscore_grade': 'str',
                     'nova_group': 'int',
                     'url': 'str',
                     'generic_name_fr': 'str',
                     'quantity': 'str',
                     'ingredients_text': 'str'}
