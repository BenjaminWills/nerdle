from collections import Counter

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

Example:

Suppose the equation we're trying to guess is: 56/8-3=4

1.12+10=22 # No guesses are in common
2.
3.
4.
5.
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

    lhs, rhs = guess.split("=")

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

    if evaluated_lhs != evaluated_rhs:
        ValueError(
            "Left hand side of the equation does not equal the right hand side of the equation."
        )
    return space_removed_guess


def evaluate_guess(guess: str, target: str, previous_state: str = None):
    state = ["X"] * 8
    formatted_guess = validate_guess(guess)
    # Find all indices of the guess and target that intersect, these will be coloured green.
    # Find all characters in the guess that are in different indices but are present in the target
    for index, (guess_char, target_char) in enumerate(zip(formatted_guess, target)):
        if guess_char == target_char:
            state[index] = guess_char
        else:
            if guess_char in target:
                state[index] = "G"
    # Join the state
    state_str = "".join(state)
    return state_str


class Nerdle:
    def __init__(self) -> None:
        pass

    def __init_board(
        self,
    ):
        pass

    def make_guess(
        self,
    ):
        pass

    def update_board(
        self,
    ):
        pass


if __name__ == "__main__":
    target = "56/8-4=3"
    guess = "56/7-3=4"
    print(evaluate_guess(guess, target))
