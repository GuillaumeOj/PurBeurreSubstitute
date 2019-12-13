"""
    This module manage all operations with the database
"""
import mysql.connector


class Database:
    """
        This class manage differents operations with the database like:
            - connection
            - insert data
            - remove data
            - select data
    """

    def __init__(self, user, host, password):
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
            self.cursor.execute('USE PBS')
        except mysql.connector.Error as err:
            print(err)

    def check_database(self):
        """
            This method check if the database is empty
            If it is, run a method for filling it
        """
        try:
            query = 'SELECT * FROM Products LIMIT 1'
            response = self.cursor.execute(query)
        except mysql.connector.Error as err:
            print(err)

        if not response:
            return False

        return True

if __name__ == '__main__':
    print('Please don\'t load me alone...')
