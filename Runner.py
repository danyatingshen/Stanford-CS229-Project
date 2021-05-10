from QL import MDP
import random

def main():
    mdp = MDP()
    curr_state = mdp.startState()
    reward = mdp.reward(curr_state)
    #print("state state: ", curr_state)
    # ------------------------------------
    random.seed(12345)
    while True:
        print("state: ", curr_state)
        action = random.choice(mdp.actions(curr_state))
        print("action: ", action)
        next_state = mdp.successor(curr_state, action)
        print(next_state)

        reward = mdp.reward(next_state)
        curr_state = next_state

if __name__ == '__main__':
    main()
