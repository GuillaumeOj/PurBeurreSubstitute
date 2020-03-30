"""
    This module display a list of answers as a menu
"""
import termtables


class SelectionMenu:
    """
        Easy object for display a menu:
            - Possible answers
            - Manage user input
            - Give the user choice in the 'selected' property
    """

    def __init__(self, menu_title, answer_title, answers):
        self.menu_title = menu_title
        self.answer_title = answer_title
        self.answers = answers

        # Count the answers' number
        if isinstance(self.answers, tuple):
            self.answers_count = len(self.answers[0])
        else:
            self.answers_count = len(self.answers)

        self.user_choice = 0

        while self.user_choice == 0:
            self.display_answers()
            self.user_input()

    @property
    def selected(self):
        """
            This method return the answer choose by the user
        """
        if isinstance(self.answers, tuple):
            return self.answers[1][self.user_choice - 1]

        return self.answers[self.user_choice - 1]

    def display_answers(self):
        """
            This method display the answers as a numbered list
        """
        print('')
        title = f'=== {self.menu_title} ==='
        print(title)

        # This statement is for manage two list sent in a tuple
        if isinstance(self.answers, tuple):
            to_substitute_list = self.answers[0]
            substituted_list = self.answers[1]

            zip_list = zip(to_substitute_list, substituted_list)
            table_header = ['',
                            'Produit à substituer',
                            'Produit de substitut']
            table_data = list()

            for i, (to_substitute, substituted) in enumerate(zip_list):
                line = [f'{i + 1}.',
                        to_substitute['name'],
                        substituted['name']]
                table_data.append(line)
            if table_data:
                termtables.print(
                    table_data,
                    header=table_header,
                    style=termtables.styles.ascii_thin,
                    padding=(0, 1),
                    alignment='lll')
            else:
                print('Pas de substitut enregistré')
        else:
            table_header = []
            table_data = []
            for i, choice in enumerate(self.answers):
                # This statement is for a simple string answer
                if isinstance(choice, str):
                    line = [f'{i + 1}.',
                            choice]
                    if len(table_header) > 2:
                        blank_to_add = len(table_header) - len(line)
                        for _ in range(blank_to_add):
                            line.append('')
                    table_data.append(line)
                # This statement is for an answer sent as a dict
                if isinstance(choice, dict):
                    if not table_header:
                        table_header = ['',
                                        'Nom du produit',
                                        'Nutriscore',
                                        'Code barre']
                    line = [f'{i + 1}.',
                            choice['name'],
                            choice['nutriscore_grade'],
                            str(choice['code'])]
                    table_data.append(line)

            termtables.print(
                table_data,
                header=table_header,
                style=termtables.styles.ascii_thin)

    def user_input(self):
        """
            This method ask the user to give an answer
        """
        title = f'-> {self.answer_title} : '
        try:
            self.user_choice = int(input(title))
            assert 1 <= self.user_choice <= self.answers_count
        except AssertionError:
            print(f'Merci de donner un nombre entre 1 et {self.answers_count}')
            self.user_choice = 0
        except ValueError:
            print('Le choix doit être un nombre entier')


if __name__ == '__main__':
    print('Please don\'t load me alone...')
