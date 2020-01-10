"""
    This module define a product and all method associated
"""


class Product: # pylint: disable=too-many-instance-attributes
    """
        This class allow to create a structred object with many arguments
    """

    products = list()

    def __init__(self, **kwargs):
        self.categories = kwargs['categories']
        self.code = kwargs['code']
        self.name = kwargs['product_name']
        self.nutriscore_grade = kwargs['nutriscore_grade']
        self.url = kwargs['url']

        self.common_name = str()
        self.quantity = str()
        self.ingredients_text = str()
        self.brands = list()
        self.stores = list()

        if 'generic_name_fr' in kwargs:
            self.common_name = kwargs['generic_name_fr']
        if 'common_name' in kwargs:
            self.common_name = kwargs['common_name']
        if 'quantity' in kwargs:
            self.quantity = kwargs['quantity']
        if 'ingredients_text' in kwargs:
            self.ingredients_text = kwargs['ingredients_text']
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

        print(f'Nutriscore : {self.nutriscore_grade.upper()}')

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
