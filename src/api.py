"""
    This module manage all operations with the api:
"""
import os
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
        """
            Initialize the object with some basics informations
        """

        self.url_base = url_base
        self.tmp_dir = tmp_dir
        self.categories = list()
        self.page_size = int()
        self.pages = int()

        # Create a tmp/ directory
        try:
            os.mkdir(self.tmp_dir)
        except FileExistsError:
            print(f'Directory "{self.tmp_dir}" already exist')

    def download_products(self, categories, page_size, pages):
        """
            Download products in temp json files
        """
        self.categories = categories
        self.page_size = page_size
        self.pages = pages

        for category in self.categories:
            try:
                dir_path = os.path.join(self.tmp_dir, category)
                os.mkdir(dir_path)
            except FileExistsError:
                print(f'Directory "{dir_path}" already exist')

            # Headers for the request see : https://en.wiki.openfoodfacts.org/API/Read/Search
            headers = {'User-agent': 'PurBeurreSubstitute - Mac OS X 10.13 - Version 1.0'}

            # Just a little progress bar for seeing the application work
            progress_bar = FillingCirclesBar(f'Downloading in {dir_path}: ', max=self.pages)
            for page in range(self.pages):
                # Parameters sent with te request
                parameters = {'json': 1,
                              'page_size': self.page_size,
                              'page': page,
                              'categorie': category,
                              'action': 'process'}

                # File in wich data are saved
                file_name = f'{page}.json'
                file_path = os.path.join(dir_path, file_name)

                with open(file_path, 'w') as output_file:
                    # Load data
                    try:
                        response = requests.get(self.url_base,
                                                params=parameters,
                                                headers=headers,
                                                stream=True)
                        response.raise_for_status()
                    except requests.HTTPError as err:
                        print(err)

                    # Write data in a json format
                    json.dump(response.json(), output_file, indent=4)
                progress_bar.next()
            progress_bar.finish()
        print('Downloading done!')

    def delete_files(self):
        """
            This method is called for deleting tmp files
        """
        rmtree(self.tmp_dir)

        print('Temp data removed.')




if __name__ == '__main__':
    print('Please don\'t load me alone...')
