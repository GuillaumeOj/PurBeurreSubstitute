"""
    This module define a product and all method associated
"""


class Product:
    """
        This class allow to create a structred object with many arguments
    """
    products = list()
    def __init__(self, **arguments):
        for argument, value in arguments.items():
            setattr(self, argument, value)

        Product.products.append(self)


if __name__ == '__main__':
    print('Please don\'t load me alone...')
