from QL import MDP
import random

def main():
    mdp = MDP()
    curr_state = mdp.startState()
    #next_state =
    print("state state: ", curr_state)
    # ------------------------------------


    while True:
        # print("state: ", curr_state)
        action = random.choice(mdp.actions(curr_state))
        print("action: ", action)
        next_state = mdp.successor(curr_state, action)
        reward = mdp.reward(curr_state, action, next_state)
        print("next state ", next_state)
        curr_state = next_state
        print("")

if __name__ == '__main__':
    main()
