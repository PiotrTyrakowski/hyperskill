import os
import builtins
from io import StringIO
import argparse

# Create an argument parser for the program
parser = argparse.ArgumentParser(description="Flash Card Creator")
parser.add_argument("--import_from", default=None)  # Argument to specify the file to import flash cards from
parser.add_argument("--export_to", default=None)  # Argument to specify the file to export flash cards to
args = parser.parse_args()

# Create a memory file to store print statements and user inputs
memory_file = StringIO()


def my_print(*args, **kwargs):
    """
    Custom print function that writes the output to the memory file in addition to printing it.
    """
    # Convert the arguments to strings
    output = ' '.join(str(arg) for arg in args)

    # Perform the original print functionality
    builtins.print(*args, **kwargs)

    # Write the output to the memory file
    memory_file.write(output + '\n')


def my_input(prompt=''):
    """
    Custom input function that writes the user input to the memory file.
    """
    # Perform the original input functionality
    user_input = builtins.input(prompt)

    # Write the input to the memory file
    memory_file.write(f"{user_input}\n")

    return user_input


class FlashCard:
    """
    Class representing a flash card with a term, definition, and error count.
    """
    def __init__(self, term, definition, error):
        self.term = term
        self.definition = definition
        self.error = error


class FlashCardApp:
    """
    Class representing a flash card application.
    """
    def __init__(self):
        self.cards = []

    def add_card(self, term, definition, error=0):
        """
        Add a new flash card to the application.
        """
        self.cards.append(FlashCard(term, definition, int(error)))

    def add(self):
        """
        Add a new flash card by prompting the user for the term and definition.
        """
        my_print("The card:")

        while True:
            term = my_input()
            term_exists = False

            # Check if the term already exists in the flash cards
            for card in self.cards:
                if card.term == term:
                    my_print(f'The card "{term}" already exists. Try again:')
                    term_exists = True
                    break

            if not term_exists:
                break

        while True:
            definition = my_input()
            definition_exists = False

            # Check if the definition already exists in the flash cards
            for card in self.cards:
                if card.definition == definition:
                    my_print(f'The definition "{definition}" already exists. Try again:')
                    definition_exists = True
                    break

            if not definition_exists:
                break

        my_print(f'The pair ("{term}":"{definition}") has been added.')
        self.add_card(term, definition)

    def remove_card(self, term):
        """
        Remove a flash card from the application based on the term.
        """
        self.cards = [card for card in self.cards if card.term != term]

    def remove(self):
        """
        Remove a flash card by prompting the user for the term.
        """
        my_print('Which card?')
        user_input = my_input()

        for card in self.cards:
            if user_input == card.term:
                self.remove_card(user_input)
                my_print('The card has been removed.')
                return

        my_print(f'Can\'t remove "{user_input}": there is no such card.')

    def import_from_file(self, file_path):
        """
        Import flash cards from afile into the application.
        """
        if not os.path.isfile(file_path):
            my_print('File not found.')
        else:
            number_of_cards = 0
            with open(file_path, "r") as file:
                for line in file:
                    # Split the line into term, definition, and error count
                    term, definition, error = line.strip().split()

                    # Remove the card if it already exists in the stack
                    self.remove_card(term)

                    # Add the card to the application
                    self.add_card(term, definition, error)
                    number_of_cards += 1
            my_print(f'{number_of_cards} cards have been loaded.')

    def import_cards(self):
        """
        Prompt the user for the file name and import flash cards from the file.
        """
        my_print('File name:')
        file_name = my_input()
        file_path = "./" + file_name
        self.import_from_file(file_path)

    def export_to_file(self, file_path):
        """
        Export flash cards from the application to a file.
        """
        with open(file_path, "w") as file:
            for card in self.cards:
                line = f"{card.term} {card.definition} {card.error}\n"
                file.write(line)
        my_print(f'{len(self.cards)} cards have been saved.')

    def export_cards(self):
        """
        Prompt the user for the file name and export flash cards to the file.
        """
        my_print('File name:')
        file_name = my_input()
        file_path = "./" + file_name
        self.export_to_file(file_path)

    def ask(self):
        """
        Ask the user to define the terms of flash cards and provide feedback on correctness.
        """
        number_of_cards = len(self.cards)
        if number_of_cards == 0:
            my_print('There are 0 cards in the stack')
            return
        my_print('How many times to ask?')
        n = int(my_input())

        for i in range(n):
            current_card = i % number_of_cards

            my_print(f'Print the definition of "{self.cards[current_card].term}":')
            user_input = my_input()
            if user_input == self.cards[current_card].definition:
                my_print("Correct!")
            else:
                self.cards[current_card].error += 1
                correct_definition_for_other = False

                # Check if the user's definition matches any other term
                for card in self.cards:
                    if card.definition == user_input:
                        my_print(f'Wrong. The right answer is "{self.cards[current_card].definition}", but your definition is correct for "{card.term}".')
                        correct_definition_for_other = True
                        break
                if not correct_definition_for_other:
                    my_print(f'Wrong. The right answer is "{self.cards[current_card].definition}".')

    def log(self):
        """
        Save the memory file to a log file specified by the user.
        """
        my_print("File name:")
        file_name = my_input()

        # Seek to the beginning of the memory file
        memory_file.seek(0)
        with open(file_name, "w") as log:
            for line in memory_file:
                log.write(line)
        my_print("The log has been saved.")

    def hardest_card(self):
        """
        Determine the flash card(s) with the highest error count and display them.
        """
        sorted_cards = sorted(self.cards, key=lambda card: card.error, reverse=True)

        if len(self.cards) == 0 or sorted_cards[0].error == 0:
            my_print("There are no cards with errors.")
        else:
            st = f'"{sorted_cards[0].term}"'
            plural_form = False
            for i in range(1, len(sorted_cards)):
                if sorted_cards[i].error != sorted_cards[0].error:
                    break

                plural_form = True
                st = st + f', "{sorted_cards[i].term}"'

            if plural_form:
                my_print(f'The hardest cards are {st}. You have {sorted_cards[0].error} errors answering them.')
            else:
                my_print(f'The hardest card is {st}. You have {sorted_cards[0].error} errors answering it.')

    def reset_stats(self):
        """
        Reset the error count for all flash cards.
        """
        for card in self.cards:
            card.error = 0
        my_print('Card statistics have been reset.')


def main():
    """
    Main function to handle user input and execute actions.
    """
    flash_card_app = FlashCardApp()

    # Import flash cards from a file if specified in the command line arguments
    if args.import_from is not None:
        file_name = args.import_from
        file_path = "./" + file_name
        flash_card_app.import_from_file(file_path)

    # Define the available actions
    action = {
        'add': flash_card_app.add,
        'remove': flash_card_app.remove,
        'import': flash_card_app.import_cards,
        'export': flash_card_app.export_cards,
        'ask': flash_card_app.ask,
        'log': flash_card_app.log,
        'hardest card': flash_card_app.hardest_card,
        'reset stats': flash_card_app.reset_stats
    }

    while True:
        my_print("Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):")
        user_input = my_input()
        if user_input in action:
            action[user_input]()
        elif user_input == 'exit':
            my_print('Bye bye!')
            break
        else:
            my_print(f'There is no action {user_input}, please try again')

    # Export flash cards to a file if specified in the command line arguments
    if args.export_to is not None:
        file_name = args.export_to
        file_path = "./" + file_name
        flash_card_app.export_to_file(file_path)



if __name__ == "__main__":
    main()
