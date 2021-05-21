import operator
import random
import re

import FeatureExtractor


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


def create_problem(state,bins):
    try:
        new_problem = random.choice(bins[state])
        return Problem(new_problem[0], new_problem[1])
    except:
        raise Exception('Cannot find matching tuple in problem bank for next state : ', state)


def is_success(state, action):
    map = {(1, 1, 0, 0, 0):((1,2),(1,3))}
    if type(state) is not tuple or type(action) is not tuple:
        return
    observed_states = state[0]
    if len(observed_states) != len(action):
        return

    new_state = next_sate(observed_states, action)
    problem = create_problem(new_state, map)
    return new_state, problem


state, prob = is_success(((1, 0, 0, 0, 0),(1,2,3,4,5)), (0, 1, 0, 0, 0))

print("State: ", state)
print("Problem: ", prob.x, " + ", prob.y)
