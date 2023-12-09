import random
import time
import string

WORDLIST_FILENAME = "words.txt"
SECRET_LETTER = '?'

DRAWINGS = [
    " _____\n |   |\n O   |\n/|\  |\n |   |\n/ \  |\n_______|__",
    " _____\n |   |\n O   |\n/|\  |\n |   |\n  \  |\n_______|__",
    " _____\n |   |\n O   |\n/|\  |\n |   |\n     |\n_______|__",
    " _____\n |   |\n O   |\n |\  |\n |   |\n     |\n_______|__",
    " _____\n |   |\n O   |\n |   |\n |   |\n     |\n_______|__",
    " _____\n |   |\n O   |\n     |\n     |\n     |\n_______|__",
    " _____\n |   |\n     |\n     |\n     |\n     |\n_______|__",
]

INITIAL_GUESSES = len(DRAWINGS) - 1


def load_words():
    print("\nLoading word list from file...")
    in_file = open(WORDLIST_FILENAME, 'r')
    line = in_file.readline()
    words = line.split()
    print("...", len(words), "words loaded.\n")
    return words


wordlist = load_words()


def choose_word():
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    return get_guessed_word(secret_word, letters_guessed) == secret_word


def get_guessed_word(secret_word, letters_guessed):
    masked = ''
    for letter in secret_word:
        masked += SECRET_LETTER if letter not in letters_guessed else letter
    return masked


def get_available_letters(letters_guessed):
    return '' .join([l if l not in letters_guessed else '' for l in string.ascii_lowercase])


def align_center(s):
    width = len(string.ascii_lowercase)
    spaces = (width - len(s)) // 2
    return ' ' * spaces + s + ' ' * (width - len(s) - spaces)


def match_with_gaps(my_word, other_word, letters_guessed=''):
    my_word = my_word.replace(" ", "")

    if len(my_word) != len(other_word):
        return False

    for i in range(0, len(my_word)):

        letter = my_word[i]
        if letter == SECRET_LETTER:
            if other_word[i] in letters_guessed:
                return False

        if letter != SECRET_LETTER:
            if other_word[i] != letter:
                return False

    return True


def show_possible_matches(my_word, letters_guessed=''):
    print("Possible word matches are:", end=' ')
    for i in range(0, len(wordlist)):
        if match_with_gaps(my_word, wordlist[i], letters_guessed):
            print(wordlist[i], end=' ')


def hangman_with_hints(secret_word, with_hint=True):
    letters_guessed = []
    number_of_warnings = 3
    number_of_guesses = INITIAL_GUESSES

    def print_game_step(step_title):
        print(step_title)
        for line in DRAWINGS[number_of_guesses].split('\n'):
            print(align_center(line))
        print(f"{align_center(guessed_word_decoration())} # my secret word")
        print(f"{align_center(guesses_decoration())} # remaining lives")
        print(f"{get_available_letters(letters_guessed)} # available letters")

    def guessed_word_decoration():
        return get_guessed_word(secret_word, letters_guessed)

    def guesses_decoration():
        return number_of_guesses * '+' if number_of_guesses > 0 else '-'

    print_game_step(f"I am thinking of a word that is {len(secret_word)} letters long.")

    while number_of_guesses > 0 and not is_word_guessed(secret_word, letters_guessed):

        time.sleep(0.5)

        new_letter = str.lower(input("Please guess a letter: "))

        if with_hint and new_letter == "*":
            show_possible_matches(guessed_word_decoration(), letters_guessed)
            print()
            continue

        is_valid_letter = str.isalpha(new_letter) and len(list(new_letter)) == 1
        is_letter_used = new_letter in letters_guessed
        if is_letter_used or not is_valid_letter:

            is_warning_used = number_of_warnings > 0
            if is_warning_used:
                number_of_warnings -= 1
            else:
                number_of_guesses -= 1

            first_sentence = "You've already guessed that letter" if is_letter_used else f"'{new_letter}' is not a valid letter"
            second_sentence = f"You have {number_of_warnings} warnings left" if is_warning_used else "You have no warnings left so you lose one guess"

            print_game_step(f"Oops! {first_sentence}. {second_sentence}.")
            continue

        letters_guessed = letters_guessed + list(new_letter)
        time.sleep(0.5)
        if str.lower(new_letter) in secret_word:
            print_game_step("Good guess! Keep it up!")
        else:
            number_of_guesses -= 2 if new_letter in 'eioau' else 1
            print_game_step("Oops! The letter is not in my word")

    if is_word_guessed(secret_word, letters_guessed):
        print("\n\nCongratulations, you won!!!")
        print(f"Your total score for this game is: {number_of_guesses * len(set(list(secret_word)))}")
    else:
        print(f"\n\nThe word was {secret_word}. You dead.")


def main():
    secret_word = choose_word()
    hangman_with_hints(secret_word)


if __name__ == '__main__':
    main()
