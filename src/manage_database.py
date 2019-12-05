"""
    This module manage all operations with the database
"""
import sys

import mysql.connector


class ManageDatabase:
    """
        This class manage differents operations with the database like:
            - Connection
            - Insert data
            - Remove data
            - Select data
    """

    def __init__(self, user, host, password):
        """
            initialize the object with some important informations:
                - user name
                - host name
                - password
        """

        self.user = user
        self.host = host
        self.password = password

        # Connect to the database
        try:
            self.connection = mysql.connector.connect(
                user=self.user,
                host=self.host,
                password=self.password)

            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print(err)
            sys.exit()

if __name__ == '__main__':
    print('Please don\'t load me alone...')
