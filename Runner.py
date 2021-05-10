from QL import MDP
import random

def main():
    mdp = MDP()
    curr_state = mdp.startState()
    #print("state state: ", curr_state)
    # ------------------------------------

    visited_states = set()

    max_iter = 1000000
    for _ in range(max_iter):
        #print("state: ", curr_state)
        visited_states.add(curr_state)


        action = random.choice(mdp.actions(curr_state))
        #print("action: ", action)
        next_state = mdp.succesor(curr_state, action)
        #print(next_state)
        #reward = mdp.reward(curr_state,action,next_state)

        curr_state = next_state
        #print("")

    print(visited_states)
    print(len(visited_states))
if __name__ == '__main__':
    main()
