"""
    Settings file for PurBeurreSubstitute
"""

# MySQL informations
PBS_USER = 'pbs'
PBS_HOST = 'localhost'
PBS_PASSWORD = 'pbs'

# Temp dir in which we download data
TMP_DIR = 'tmp/'

# Parameters for download data
API_PAGE_SIZE = 100
API_PAGES = 10
API_URL_BASE = 'https://fr.openfoodfacts.org/cgi/search.pl'
API_CATEGORIES = ['aliments-d-origine-vegetale',
                  'viandes',
                  'boissons',
                  'confiseries',
                  'produits-laitiers']
API_SORT = 'product_name'
