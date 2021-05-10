from QL import MDP
import random

def main():
    mdp = MDP()
    curr_state = mdp.startState()
    #print("state state: ", curr_state)
    # ------------------------------------
    max_iter = 10000
    for _ in range(max_iter):
        print("state: ", curr_state)
        action = random.choice(mdp.actions(curr_state))
        print("action: ", action)
        next_state = mdp.successor(curr_state, action)
        print(next_state)
        #reward = mdp.reward(curr_state,action,next_state)
        curr_state = next_state

if __name__ == '__main__':
    main()
