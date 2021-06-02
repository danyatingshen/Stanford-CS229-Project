from main import MDP
import random


def main():
    mdp = MDP()
    curr_state = mdp.startState()

    visited_states = set()

    max_iter = 1000000
    for _ in range(max_iter):
        visited_states.add(curr_state)

        action = random.choice(mdp.actions(curr_state))

        next_state = mdp.succesor(curr_state, action)

        curr_state = next_state

    print(visited_states)
    print(len(visited_states))


if __name__ == '__main__':
    main()
