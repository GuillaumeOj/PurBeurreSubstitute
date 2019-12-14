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

    def attributes_to_tuple(self, attributes_order, attributes_type):
        """
            This method transfrom attributes in tuples for insertion in a database
        """
        attributes_list = list()
        for i in range(len(attributes_order)):
            attribute = attributes_order[str(i)]
            if hasattr(self, attribute):
                if getattr(self, attribute) != '' and attributes_type[attribute] == 'str':
                    attributes_list.append(getattr(self, attribute))
                elif getattr(self, attribute) != '' and attributes_type[attribute] == 'int':
                    attributes_list.append(int(getattr(self, attribute)))
                else:
                    attributes_list.append('NULL')
            else:
                attributes_list.append('NULL')

        attributes_tuple = tuple(attributes_list)

        return attributes_tuple



if __name__ == '__main__':
    print('Please don\'t load me alone...')
