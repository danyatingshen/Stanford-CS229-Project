

import MDP
import QLearning
import util
import copy

def simulate(load_q_filename=None, save_q_filename=None, sim_student_filename=None, train_mode=True, delta=.001,
             max_iter=100000, verbose=True):
    q_init = util.load_q(load_q_filename)
    sim_student = util.load_student(sim_student_filename)

    mdp = MDP.MDP()
    mdp.sim_student = sim_student
    ql = QLearning.QLearning(mdp.actions, q_init, train_mode)

    #Change Here
    Q_old = copy.deepcopy(q_init)
    for key in Q_old:
        Q_old[key] = 10
    #

    episode_rewards = []

    cur_state = mdp.start_state()
    consecutive_counter = 0
    for _ in range(max_iter):
        action = ql.getAction(cur_state)
        nxt_state = mdp.successor(cur_state, action)
        reward = mdp.reward(cur_state, action, nxt_state)
        ql.updateQ(cur_state, action, reward, nxt_state)

        cur_state = nxt_state
        episode_rewards.append(reward)

        ea = max([abs(ql.Q[key] - Q_old[key]) / (Q_old[key] if Q_old[key] != 0 else 1) for key in ql.Q])

        if ea < .01:
            consecutive_counter += 1
        else:
            consecutive_counter = 0

        if mdp.isEnd(cur_state) or consecutive_counter >= 5 and train_mode:
            break
        Q_old = copy.deepcopy(ql.Q)

    if verbose:
        print("----------------------------------------------")
        if sim_student is not None:
            print("Converged in: " + str(ql.num_iterations) + " iterations\n")

            optimal_states = sorted([(sim_student[key][0], key) for key in sim_student if sim_student[key][0] > 0], reverse=True)

            print("Optimal States:")
            print(optimal_states)

        print("\nOptimal Policy")
        optimal_policy = ql.optimalPolicy()
        for key in sorted(optimal_policy):
            print(str(key) + ": " + str(optimal_policy[key]))
        print("----------------------------------------------")

    util.save_q(save_q_filename, ql.Q)
    return ql.Q, episode_rewards


if __name__ == '__main__':
    Q_table, episode_rewards = simulate(
                                        sim_student_filename='data/student_cortney.json', train_mode=True)
