from tqdm import tqdm
import numpy as np


def generate_nerdle_solution(lhs_length: int) -> str:
    characters = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, "+", "-", "/", "*"]

    random_indices = np.random.choice(len(characters), (lhs_length))
    rhs_length = 8 - lhs_length - 1

    lhs = ""
    for index in random_indices:
        lhs += str(characters[index])

    if lhs.startswith(("+", "-", "/", "*")):
        return None
    for index in range(lhs_length - 1):
        if lhs[index] == lhs[index + 1] and lhs[index] in ["+", "-", "/", "*"]:
            return None
        if lhs[index] in ["+", "-", "/", "*"] and lhs[index + 1] in [
            "+",
            "-",
            "/",
            "*",
        ]:
            return None
        if lhs[index] == "0" and lhs[index + 1] not in ["+", "-", "/", "*"]:
            return None

    try:
        lhs_eval = eval(lhs)
        if "." in str(lhs_eval) or "-" in str(lhs_eval):
            return None

        if len(str(lhs_eval)) == rhs_length:
            return_str = f"{lhs}={lhs_eval}"
            if len(return_str) == 8:
                return return_str
            else:
                return None
        else:
            return None
    except:
        return None


def generate_nerdle_solutions(lhs_length: int, iterations: int = 100_000) -> list:
    solutions = []
    for _ in tqdm(range(iterations)):
        solution = generate_nerdle_solution(lhs_length)
        if solution is not None:
            solutions.append(solution)
    return solutions


if __name__ == "__main__":
    import json

    solutions = []
    for i in range(4, 8):
        nerdle_training_solutions = generate_nerdle_solutions(i)
        solutions.extend(nerdle_training_solutions)

    with open("train.json", "w") as training_file:
        json.dump(list(set(solutions)), training_file, indent=1)
