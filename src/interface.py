"""
    This module display a list of answers as a menu
"""


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
        title = f'\n=== {self.menu_title} ==='
        print(title)

        # This statement is for manage two list sent in a tuple
        if isinstance(self.answers, tuple):
            to_substitute_list = self.answers[0]
            substituted_list = self.answers[1]

            zip_list = zip(to_substitute_list, substituted_list)

            for i, (to_substitute, substituted) in enumerate(zip_list):
                line = f"{i + 1}. {to_substitute['name']}"
                line = f"{line} ==> Substitué par ==>"
                line = f"{line} {substituted['name']}"
                print(line)
        else:
            for i, choice in enumerate(self.answers):
                # This statement is for a simple string answer
                if isinstance(choice, str):
                    line = f"{i + 1}. {choice}"
                # This statement is for an answer sent as a dict
                if isinstance(choice, dict):
                    line = f"{i + 1}. {choice['name']}"
                    line = f"{line} | {choice['nutriscore_grade']}"
                    line = f"{line} | {choice['code']}"
                print(line)

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
