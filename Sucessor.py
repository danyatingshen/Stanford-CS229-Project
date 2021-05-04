import operator
import random
import re


class Problem:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.operation = 'operation'


def next_sate(state, action):
    try:
        return tuple(map(operator.add, state, action))
    except:
        print("exception next_sate")


def compare_tuple(a, b):
    for answer in [(a == b) for a, b in zip(a, b)]:
        if not answer:
            return False
    return True


def create_problem(state):
    with open("problemBank", "r") as param_file:
        raw = param_file.read()
        lines = re.findall(r'\(.*?\)', raw)
        if lines[0] == str(state):
            problem_lst = lines[1:]
            result = random.choice(problem_lst)
            return Problem(result[1], result[4])

    raise Exception('Cannot find matching tuple in problem bank for next state : ', state)


def is_success(state, action):
    if type(state) is not tuple or type(action) is not tuple:
        return
    observed_states = state[0]
    if len(observed_states) != len(action):
        return

    new_state = next_sate(observed_states, action)
    problem = create_problem(new_state)
    return new_state, problem


state, prob = is_success(((1, 0, 0, 0, 0),(1,2,3,4,5)), (0, 1, 0, 0, 0))

print("State: ", state)
print("Problem: ", prob.x, " + ", prob.y)
