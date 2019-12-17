"""
    This module manages the display of information for the user
"""


class SelectionMenu:
    """
        Easy object for display a menu:
            - Possible choices
            - Manage user answer
    """
    def __init__(self, *choices):
        self.choices = choices

    def display_choices(self, title):
        """
            This method display the choices on the screen
        """
        title = f'=== {title} ==='
        print(title)
        for i, choice in enumerate(self.choices):
            line = f'{i + 1}. {choice}'
            print(line)


if __name__ == '__main__':
    print('Please don\'t load me alone...')
