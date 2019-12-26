"""
    This module define a product and all method associated
"""


class Product: # pylint: disable=too-many-instance-attributes
    """
        This class allow to create a structred object with many arguments
    """

    products = list()

    def __init__(self, **kwargs):

        self.categories = None
        self.brands = None
        self.stores = None

        self.code = int(kwargs['code'])
        self.name = kwargs['product_name'][:200]
        self.nova_group = int(kwargs['nova_group'])
        self.nutriscore_grade = kwargs['nutriscore_grade'][:1]
        self.url = kwargs['url'][:250]

        self.common_name = str()
        self.quantity = str()
        self.ingredients_text = str()

        if 'generic_name_fr' in kwargs:
            self.common_name = kwargs['generic_name_fr'][:200]
        if 'common_name' in kwargs:
            self.common_name = kwargs['common_name'][:200]
        if 'quantity' in kwargs:
            self.quantity = kwargs['quantity'][:50]
        if 'ingredients_text' in kwargs:
            self.ingredients_text = kwargs['ingredients_text']
        if 'categories' in kwargs:
            self.categories = kwargs['categories']
        if 'brands' in kwargs:
            self.brands = kwargs['brands']
        if 'stores' in kwargs:
            self.stores = kwargs['stores']

        Product.products.append(self)

    @property
    def count(self):
        """
            Give the number of products
        """
        print(len(Product.products))
        return len(Product.products)

    def add_categories(self, categories):
        """
            Associate multiple categories to this product
        """
        self.categories = categories

    def add_stores(self, stores):
        """
            Associate multiple stores to this product
        """
        self.stores = stores

    def add_brands(self, brands):
        """
            Associate multiple brands to this product
        """
        self.brands = brands

    def display(self):
        """
            Display the product as a sheet
        """
        print('\n')
        print('=== Fiche produit ===')

        print(f'Nom commercial : {self.name}', end=' ')

        if self.common_name:
            print(f'// Nom générique : {self.common_name}')
        else:
            print('\n')

        print(f'Catégorie·s : {", ".join(self.categories)}')

        print(f'Code barre : {self.code}')

        print(f'Liste des ingrédients : {self.ingredients_text}')

        print(f'Quantité : {self.quantity}')

        print(f'Nutriscore : {self.nutriscore_grade.upper()}', end=' ')
        print(f'// Groupe Nova : {str(self.nova_group)}')

        if self.brands:
            print(f'Marque·s : {", ".join(self.brands)}')
        else:
            print('Marque·s : NC')

        if self.stores:
            print(f'Point·s de vente : {", ".join(self.stores)}')
        else:
            print('Point·s de vente : NC')

        print(f'Url Open Food Fact : {self.url}')



if __name__ == '__main__':
    print('Please don\'t load me alone...')
