"""
    This module manage all operations with the api:
"""
from os import path, mkdir
from shutil import rmtree
import json

import requests
from progress.bar import FillingCirclesBar


class Api:
    """
        This class manage differents operation with the api:
            - request data
            - download data
            - read data
    """

    def __init__(self, url_base, tmp_dir):
        self.url_base = url_base
        self.tmp_dir = tmp_dir
        self.categories = list()
        self.page_size = int()
        self.pages = int()
        self.data = list()

        # Create a tmp/ directory
        try:
            mkdir(self.tmp_dir)
        except FileExistsError:
            print(f'Le répertoire "{self.tmp_dir}" existe déjà')

    def download_products(self, categories, page_size, pages):
        """
            Download products in temp json files
        """

        self.categories = categories
        self.page_size = page_size
        self.pages = pages

        # Download each category
        for category in self.categories:
            try:
                dir_path = path.join(self.tmp_dir, category)
                mkdir(dir_path)
            except FileExistsError:
                print(f'Le répertoire "{dir_path}" existe déjà')

            # Headers for the request see : https://en.wiki.openfoodfacts.org/API/Read/Search
            headers = {'User-agent': 'Pur Beurre Substitute - Mac OS X 10.13 - Version 1.0'}

            # A progress bar for seeing the application working
            progress_bar = f'Téléchargement en cours de la catégorie "{category}" :'
            progress_bar = FillingCirclesBar(progress_bar, max=self.pages)
            for page in range(self.pages):
                # Parameters sent with te request
                parameters = {'json': 1,
                              'page_size': self.page_size,
                              'page': (page + 1),
                              'tagtype_0': 'categories',
                              'tag_contains_0': 'contains',
                              'tag_0': category,
                              'action': 'process'}

                # File in wich data are saved
                file_name = f'{page}.json'
                file_path = path.join(dir_path, file_name)

                with open(file_path, 'w') as output_file:
                    try:
                        result = requests.get(self.url_base,
                                              params=parameters,
                                              headers=headers,
                                              stream=True)
                        result.raise_for_status()
                    except requests.HTTPError as err:
                        print(err)

                    # Write data in a json format
                    json.dump(result.json(), output_file, indent=4)
                progress_bar.next()
            progress_bar.finish()

    def read_json_with_key(self, key):
        """
            This method read json files and return only data on specific key
        """
        progress_bar = 'Lecture des données en cours :'
        progress_bar_count = len(self.categories) * self.pages
        progress_bar = FillingCirclesBar(progress_bar, max=progress_bar_count)
        for category in self.categories:
            for page in range(self.pages):
                # Create a path for the file
                file_name = f'{page}.json'
                file_path = path.join(self.tmp_dir, category, file_name)

                # Read the JSON file
                with open(file_path, 'r') as file:
                    json_data = json.load(file)

                    # Store data in list
                    for line in json_data[key]:
                        self.data.append(line)
                progress_bar.next()
        progress_bar.finish()

    def keep_required(self, data_required):
        """
            This method drop data with missing keys
        """
        index_list = list()
        progress_bar = 'Nettoyage des produits avec données manquantes :'
        progress_bar = FillingCirclesBar(progress_bar, max=len(self.data))
        for i, dictionary in enumerate(self.data):
            try:
                for required in data_required:
                    key = required['name']
                    required = required['required']

                    # Check if the data have the required keys
                    if required and key not in dictionary:
                        raise KeyError
                    # Check if the required data are not null
                    if required and not dictionary[key]:
                        raise KeyError

            except KeyError:
                # Save the data's index if there is a key error
                index_list.append(i)
            progress_bar.next()
        progress_bar.finish()

        index_list.reverse()

        # Delete all datas with a key error
        for index in index_list:
            self.data.pop(index)

    def format_data(self, data_format):
        """
            This method format the data to the required format for the database
        """
        progress_bar = 'Formattage des données :'
        progress_bar = FillingCirclesBar(progress_bar, max=len(self.data))
        for i, dictionary in enumerate(self.data):
            for key_format in data_format:
                key = key_format['name']
                if key in dictionary:
                    data_type = key_format['type']
                    if data_type == str:
                        dictionary[key] = str(dictionary[key])
                        if 'length' in key_format:
                            length = key_format['length']
                            dictionary[key] = dictionary[key][:length]
                    elif data_type == int:
                        dictionary[key] = int(dictionary[key])
                    elif data_type == list:
                        dictionary[key] = self.string_to_list(dictionary[key])

                self.data[i] = dictionary
            progress_bar.next()
        progress_bar.finish()

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


    def delete_files(self):
        """
            This method is called for deleting tmp files
        """
        rmtree(self.tmp_dir)


if __name__ == '__main__':
    print('Please don\'t load me alone...')
