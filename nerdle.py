from collections import Counter

import numpy as np

import json

"""
The objective of Nerdle is to guess an 8 element equation. The elements of the equation can be any number 0-9 and any operation from
+,-,/,*, =. 

Rules:

- Each solution must contain exactly 1 '=' sign
- The right hand side of the equation must equal the left hand side of the equation
- No operator signs are allowed after the equals sign.
- There can never be two operator signs written side by side
- Every operator must have a numeral imediately afterwards
- Each guess must be 8 characters long
"""


def validate_guess(guess: str) -> str:
    # Format the input guess
    space_removed_guess = guess.replace(" ", "")

    # Ensure the guess is of the correct length
    if len(space_removed_guess) != 8:
        raise ValueError("Guess does not have 8 characters.")

    # Count equal signs
    element_counts = Counter(space_removed_guess)
    if element_counts.get("=", 0) != 1:
        raise ValueError("Guesses must contain exactly 1 equals sign.")

    lhs, rhs = space_removed_guess.split("=")

    # Verify that +,-,*,/ is not on the RHS
    if "+" in rhs or "-" in rhs or "*" in rhs or "/" in rhs:
        raise ValueError("Operators cannot be on the right hand side of the equation.")

    # Verify that lhs = rhs when operated on
    try:
        evaluated_lhs = eval(lhs)
    except SyntaxError:
        raise SyntaxError("The left hand side of the equation has invalid syntax.")

    try:
        evaluated_rhs = eval(rhs)
    except SyntaxError:
        raise SyntaxError("The right hand side of the equation has invalid syntax.")

    # LHS must be an integer
    if evaluated_lhs != int(evaluated_lhs) or evaluated_rhs != int(evaluated_rhs):
        raise ValueError("Result of the equation must be a positive integer")

    if evaluated_lhs != evaluated_rhs:
        raise ValueError(
            "Left hand side of the equation does not equal the right hand side of the equation."
        )

    # LHS cannot start with an operation
    if lhs.startswith(("+", "-", "/", "*")):
        raise ValueError("Left hand side of the equation cannot start with an operator")

    # Two operations cannot follow eachother
    for index in range(len(lhs) - 1):
        if lhs[index] == lhs[index + 1] and lhs[index] in ["+", "-", "/", "*"]:
            raise ValueError("Two operations cannot follow eachother")

        if lhs[index] in ["+", "-", "/", "*"] and lhs[index + 1] in [
            "+",
            "-",
            "/",
            "*",
        ]:
            raise ValueError("Two operations cannot follow eachother")
        if lhs[index] == "0" and lhs[index + 1] not in ["+", "-", "/", "*"]:
            raise ValueError("Nothing can follow a 0 that isn't an operation.")

    return space_removed_guess


class Nerdle:
    def __init__(self, target: str) -> None:
        self.state = ["X"] * 8
        self.target = validate_guess(target)
        self.guess_count = 0
        self.board = self.__init_board()
        self.guess_statistics = []
        self.guesses = []

    def __increment_guesses(self):
        self.guess_count += 1
        return None

    def __init_board(
        self,
    ):
        return np.full((5, 8), "X")

    def evaluate_guess(self, guess: str):
        formatted_guess = validate_guess(guess)
        # Find all indices of the guess and target that intersect, these will be coloured green.
        # Find all characters in the guess that are in different indices but are present in the target
        for index, (guess_char, target_char) in enumerate(
            zip(formatted_guess, self.target)
        ):
            if guess_char == target_char:
                self.state[index] = guess_char
            else:
                if guess_char in self.target:
                    self.state[index] = "G"
        # Join the state
        state_str = "".join(self.state)
        return state_str

    def __update_board(
        self,
    ):
        self.board[self.guess_count, :] = self.state
        pass

    def make_guess(self, guess: str):
        board_state = self.evaluate_guess(guess)
        self.guesses.append(guess)
        self.__update_board()
        self.__increment_guesses()
        return board_state

    def victory_condition(self):
        if "X" not in self.state and "G" not in self.state:
            return True
        else:
            return False

    def calculate_guess_statistics(self):
        pass

    def input_guess(
        self,
        prompt: str = "Please make a guess below. Remember guesses should be 8 characters long and can include spaces. \n",
    ) -> str:
        try:
            guess = input(prompt)
            self.make_guess(guess)
        except Exception as e:
            guess = self.input_guess(
                f"The previous guess caused the following error: {e} Please guess again. \n"
            )
        return guess

    def play(self) -> None:
        print("Welcome to command line Nerdle!")
        while True:
            self.input_guess()
            print(self.board)

            if self.victory_condition() == True:
                print(
                    f"Correct, you win! You got the answer in {self.guess_count} guesses."
                )
                # print(json.dumps(self.guess_statistics, indent=2))
                break

            if self.guess_count == 5:
                print("You have made too many guesses. You lose.")
                # print(json.dumps(self.guess_statistics, indent=2))
                break


if __name__ == "__main__":
    target = "56/8-4=3"
    guess = "56/7-3=4"

    nerdle = Nerdle(target)
    nerdle.play()
