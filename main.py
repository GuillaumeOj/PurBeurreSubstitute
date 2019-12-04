"""
    Main part for using Pur Beurre Substitute
    This application is made for the project 5 on OpenClassrooms during the Python courses
    The aim of this project is to use:
        - an API Rest,
        - a database like MySQL,
        - and of course Python.
"""
import sys

import mysql.connector


def main():
    """
        Main function for running the application
    """

    # Connect to the database
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='pbs',
            password='pbs')
        cursor = connection.cursor()
        cursor.execute('USE PBS')
    except mysql.connector.Error as err:
        print(err)
        sys.exit()


    # Check if there is some products in database
    try:
        query = 'SELECT * FROM Products LIMIT 1'
        products = cursor.execute(query)
        if not products:
            # Run the database filling!
            pass
    except mysql.connector.Error as err:
        print(err)
        sys.exit()


if __name__ == '__main__':
    main()
