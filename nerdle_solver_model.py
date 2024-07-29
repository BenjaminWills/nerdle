"""
Solving nerdle using information theory.

Some notes:

1. The state of a nerdle at each guess is given by a list of length 8 denoting the known characters, misplaced characters and unknown
    characters e.g ['X','X','G',1,'=','1','2','3'].

The goal right now: Make a simple model that understands how to remove numbers from the state space.
"""

import numpy as np

from utilities import factorial
from nerdle import Nerdle, validate_guess

from typing import List, Dict
from tqdm import tqdm

STATE = List[str | int]
STATE_HISTORY = List[STATE]
GUESS_HISTORY = List[str]

AVAILABLE_CHARACTERS = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "+",
    "-",
    "*",
    "/",
    "=",
]
MISSING_CHARACTER = "X"
IN_ANSWER_CHARACTER = "G"


def maximum_state_space_size(state: STATE) -> int:
    # Given a state we an find the number of unknowns, naievely we need only consider all
    # 'X' and 'G' (a bit more nuanced)
    running_product = 1
    for element in state:
        if element == "X":
            running_product *= factorial(13)
    return running_product


def get_available_guesses(
    state_history: STATE_HISTORY, guess_history: GUESS_HISTORY
) -> Dict[int, List[int | str]]:
    """We want to look between consecutive states. See below for some example states
    [
        ['5' '6' '/' 'X' '-' '4' '=' 'G'],
        ['5' '6' '/' 'G' '-' 'G' 'G' 'G'],
        ['5' '6' '/' '8' '-' 'G' '=' 'G'],
        ['5' '6' '/' '8' '-' '4' '=' '3'],
        ['X' 'X' 'X' 'X' 'X' 'X' 'X' 'X']
    ]

    We want to make a conclusion given on this state history.

        Parameters
        ----------
        state_history : STATE_HISTORY
            _description_

        Returns
        -------
        Dict[int, List[int | str]]
            _description_
    """
    # Make all available characters a list

    available_guesses = {
        character_index: AVAILABLE_CHARACTERS.copy() for character_index in range(1, 7)
    }

    # To reduce the sample spave size remove all operations from the first and last characters
    available_guesses[0] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    available_guesses[7] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for guess_index, state in enumerate(state_history):
        guess = guess_history[guess_index]
        for character_index, character in enumerate(state):
            # In the case where a guess is in the correct location
            if character in AVAILABLE_CHARACTERS:
                # print(
                #     f"Character at index {character_index} is correct with vaulue: {character}"
                # )
                available_guesses[character_index] = character
                if character == "=":
                    for key in available_guesses:
                        if (
                            type(available_guesses[key]) == list
                            and "=" in available_guesses[key]
                        ):
                            available_guesses[key].remove("=")

            # In the case where a character has been guessed but is wrong.
            if character in [MISSING_CHARACTER, IN_ANSWER_CHARACTER]:
                # We remove the possible numbers from the state space
                guessed_character = guess[character_index]
                # Remove the guessed character from the available list of characters
                if guessed_character in available_guesses[character_index]:
                    # print(
                    #     f"Character at index {character_index} is incorrect with vaulue: {guessed_character} and thus will be removed from the list"
                    # )
                    available_guesses[character_index].remove(guessed_character)

    return available_guesses


def generate_valid_guess_from_available_ones(available_guesses):
    # Run the code until it is valid
    max_iter = 10_000
    iter_count = 0
    while True:
        guess = {}
        for character_index, available_characters in available_guesses.items():
            if type(available_characters) == list:
                random_char = np.random.choice(available_characters, 1)[0]
            else:
                random_char = available_characters
            guess[character_index] = str(random_char)
        guess = "".join(dict(sorted(guess.items())).values())
        iter_count += 1
        if iter_count == max_iter:
            return "21+69=90"
        try:
            guess = validate_guess(guess)
            return guess
        except:
            continue


def naive_guesser(target: str, initial_guess: str = None) -> str | None:
    # This function will play up to 5 rounds of nerdle using the available guesses as a basis.
    nerdle = Nerdle(target)
    # Make a random initial guess.
    initial_guess = initial_guess or "46*6=276"
    nerdle.make_guess(initial_guess)
    for guessing_round in range(1, 5):
        state_history = nerdle.board[:guessing_round, :]
        guess_history = nerdle.guesses
        available_guesses = get_available_guesses(state_history, guess_history)
        # From the available guesses, generate a guess
        guess = generate_valid_guess_from_available_ones(available_guesses)
        nerdle.make_guess(guess)
        if nerdle.victory_condition():
            return guessing_round + 1

    return -1


if __name__ == "__main__":
    # target = "56/8-4=3"
    import json
    from multiprocessing import Pool, cpu_count
    import numpy as np

    with open("train.json", "r") as testing_targets_file:
        testing_targets = json.load(testing_targets_file)

    guess_counts = []

    batches = np.array_split(testing_targets, 1000)[:10]

    for batch in tqdm(batches):
        with Pool(cpu_count()) as p:
            guess_counts.extend(p.map(naive_guesser, batch))

    guess_counts = np.array(guess_counts)

    print(
        f"""
    Average number of guesses: {guess_counts[np.where(guess_counts != -1)[0]].mean()}
    Standard deviation of guesses: {guess_counts[np.where(guess_counts != -1)[0]].std()}
    Successful guesses: {len(np.where(guess_counts != -1)[0])}
    Unsucessful guesses: {len(np.where(guess_counts == -1)[0])}
"""
    )
