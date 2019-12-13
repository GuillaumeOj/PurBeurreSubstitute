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
API_LANG = 'fr'

# Required keys for each products
REQUIRED_KEYS = ['product_name',
                 'code',
                 'nutriscore_grade',
                 'nova_group',
                 'url',
                 'categories_lc']

REQUIRED_VALUES = {'categories_lc': 'fr'}
