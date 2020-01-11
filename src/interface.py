"""
    This module manages the display of information for the user
"""


class SelectionMenu:
    """
        Easy object for display a menu:
            - Possible choices
            - Manage user answer
    """
    def __init__(self, choices):
        self.choices = choices
        self.user_choice = 0

    @property
    def selected(self):
        """
            This method give the choice's name choose by the user
        """
        return self.choices[self.user_choice - 1]

    def display_choices(self, title):
        """
            This method display the choices on the screen
        """
        title = f'\n=== {title} ==='
        print(title)
        if isinstance(self.choices, tuple):
            to_substitute_list = self.choices[0]
            substituted_list = self.choices[1]

            i = 1

            for to_substitute, substituted in zip(to_substitute_list, substituted_list):
                line = f"{i}. {to_substitute['name']}"
                line = f"{line} ==> Substitué par ==>"
                line = f"{line} {substituted['name']}"
                i += 1
                print(line)
        else:
            for i, choice in enumerate(self.choices):
                if isinstance(choice, str):
                    line = f'{i + 1}. {choice}'
                if isinstance(choice, dict):
                    line = f"{i + 1}. {choice['name']}"
                    line = f"{line} | {choice['nutriscore_grade']}"
                    line = f"{line} | {choice['code']}"
                print(line)

    def user_input(self, title):
        """
            This method manage the user answer
        """
        title = f'-> {title} : '
        while self.user_choice == 0:
            try:
                self.user_choice = int(input(title))
                assert 1 <= self.user_choice <= len(self.choices)
            except AssertionError:
                print('Merci de donner une réponse correcte')
                self.user_choice = 0
            except ValueError:
                print('Le choix doit être un nombre entier')



if __name__ == '__main__':
    print('Please don\'t load me alone...')
