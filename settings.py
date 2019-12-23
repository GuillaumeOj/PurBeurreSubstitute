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
API_PAGE_SIZE = 100
API_PAGES = 10
API_URL_BASE = 'https://fr.openfoodfacts.org/cgi/search.pl'
API_CATEGORIES = ['Aliments d\'origine végétale',
                  'Viandes',
                  'Boissons',
                  'Confiseries',
                  'Produits laitiers']
API_REQUIRED_KEYS = ['product_name',
                     'code',
                     'categories',
                     'nutriscore_grade',
                     'nova_group',
                     'url']
