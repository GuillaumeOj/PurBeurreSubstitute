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
        self.id_ext = None
        self.name = None
        self.common_name = None
        self.quantity = None
        self.ingredients = None
        self.nova = None
        self.nutriscore = None
        self.url = None

        if 'categories' in kwargs:
            self.categories = self.string_to_list(kwargs['categories'])
        if 'brands' in kwargs:
            self.brands = self.string_to_list(kwargs['brands'])
        if 'stores' in kwargs:
            self.stores = self.string_to_list(kwargs['stores'])
        if 'code' in kwargs:
            self.id_ext = int(kwargs['code'])
        if 'product_name' in kwargs:
            self.name = kwargs['product_name'][:200]
        if 'generic_name_fr' in kwargs:
            self.common_name = kwargs['generic_name_fr'][:200]
        if 'quantity' in kwargs:
            self.quantity = kwargs['quantity'][:50]
        if 'ingredients_text' in kwargs:
            self.ingredients = kwargs['ingredients_text']
        if 'nutriscore_grade' in kwargs:
            self.nutriscore = kwargs['nutriscore_grade'][:1]
        if 'nova_group' in kwargs:
            self.nova = int(kwargs['nova_group'])
        if 'url' in kwargs:
            self.url = kwargs['url'][:250]

        Product.products.append(self)

    @staticmethod
    def string_to_list(string, separator=','):
        """
            This method transform an attribute from a string to a list
        """
        # Transform the string to a list of attributes
        list_of_attributes = string.split(separator)
        for i, attribute in enumerate(list_of_attributes):
            attribute = attribute.strip()
            if attribute:
                list_of_attributes[i] = attribute
            else:
                list_of_attributes.pop(i)

        return list_of_attributes


if __name__ == '__main__':
    print('Please don\'t load me alone...')
