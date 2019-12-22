"""
    Module with genereic functions for the application Pur Beurre Substitute
"""

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
