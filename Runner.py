from QL import MDP


def main():
    mdp = MDP()
    start_state = mdp.startState()
    print("state state: ", start_state)
    # ------------------------------------
    # assume action
    action = (2, 2, 1, 1, '')
    # ------------------------------------
    next = mdp.successor(start_state, action)
    print(next[1][0].x, next[1][0].y)
    print(next)

    while True:
        next = mdp.successor(next, (0, 1, 0, 0, ''))
        print(next)

if __name__ == '__main__':
    main()
