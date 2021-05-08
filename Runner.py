from QL import MDP
import random

def main():
    mdp = MDP()
    curr_state = mdp.startState()
    #print("state state: ", curr_state)
    # ------------------------------------
    while True:
        print("state state: ", curr_state)
        action = random.choice(mdp.actions(curr_state))
        reward = mdp.reward(curr_state)
        next_state = mdp.successor(curr_state, action)
        curr_state = next_state

    # ------------------------------------
    #print(next[1][0].x, next[1][0].y)
   # print(next)

    while True:
        next = mdp.successor(next, (0, 1, 0, 0, ''))
        print(next)

if __name__ == '__main__':
    main()
