"""
    This module provide general functions for the application PurBeurreSubstitute
"""

def clear_data(dataset, *required_keys, **required_values):
    """
        Function for remove products without required keys
    """
    for i, data in enumerate(dataset):
        removed = False
        for key in required_keys:
            if not key in data.keys():
                dataset.pop(i)
                # print(f'Product remove because "{key}" is not defined.')
                removed = True
                break
        if not removed:
            for key, value in required_values.items():
                if data[key] != value:
                    dataset.pop(i)
                    # print(f'Product remove because "{key}" is not equal to "{value}"')
                    removed = True
                    break

    return dataset

def string_to_list(string, separator=','):
    """
        This function transform a string into a list and clean the data for using with SQL requests
    """
    list_of_elements = string.split(separator)
    for i, element in enumerate(list_of_elements):
        element = element.strip()
        if element:
            list_of_elements[i] = (element,)
        else:
            list_of_elements.pop(i)

    return list_of_elements



if __name__ == '__main__':
    print('Please don\'t load me alone...')
