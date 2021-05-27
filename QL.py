import operator
import random
import ujson
import util
import math
import copy
import ast


class MDP:
    def __init__(self):
        self.bins = ujson.load(open('problemBank.json', 'r'))
        self.FEATURE_TUPLE_LIMIT = self.bins['state_limit']
        self.num_states = self.bins['num_states']
        self.BASE_PROBLEM_KEY = tuple([-1] * self.num_states)
        self.number_of_passed = 1
        self.problem = None
        self.curr_state_response_time = 0

        self.status = None
        self.sim_student = None

    def start_state(self):
        self.problem = (random.choice(self.bins[str(self.BASE_PROBLEM_KEY)]))
        return self.BASE_PROBLEM_KEY

    def actions(self, state):
        valid_actions = list()
        stay = tuple([0] * self.num_states)

        valid_actions.append(stay)
        # if BASE_PROBLEM_KEY the next problem will (deterministically) be a 1-digit + 1-digit (no carry op) question
        if state == self.BASE_PROBLEM_KEY:
            valid_actions.append((2, 2, 1, 1))
            return valid_actions
        # otherwise we can try to increment/decrement every feature
        for i in range(self.num_states):
            for j in [-1, 1]:
                if state[i] + j in self.FEATURE_TUPLE_LIMIT[i]:
                    action = tuple([j if k == i else 0 for k in range(self.num_states)])
                    if str(tuple(map(operator.add, state, action))) in self.bins.keys():
                        valid_actions.append(action)
        return valid_actions

    def successor(self, state, action):
        nxt_state = tuple(map(operator.add, state, action))
        self.problem = random.choice(self.bins[str(nxt_state)])
        self.number_of_passed += 1
        return nxt_state

    def reward(self, state, action, next_state):
        reward = 0
        if self.sim_student is not None:
            val, nxt_state_response_time = util.students(self.sim_student, next_state, self.problem)
        else:
            val, nxt_state_response_time = util.usr_input(self.problem)

        response = nxt_state_response_time - self.curr_state_response_time

        self.curr_state_response_time = nxt_state_response_time

        if val == 'q':
            if self.sim_student is None:
                self.status = 'Quit'
            return 0

        if val == 'n':
            reward = -abs(response)
            if self.sim_student is None:
                self.status = 'Next'
            print("Next Question!")

        if val != 'q' and val != 'n':
            if int(val) == (self.problem[0] + self.problem[1]):
                reward = response
                if self.sim_student is None:
                    print("Correct! it took you " + str(int(reward)) + " seconds longer than the last problem!")
            else:
                reward = -abs(response)
                if self.sim_student is None:
                    print("Incorrect !it took you " + str(int(reward)) + " seconds longer than the last problem!")

        return reward

    def isEnd(self, state):
        if self.status == 'Quit':
            return True
        else:
            return False


class QLearning:
    def __init__(self, mdp_actions, q_init, train_mode):
        self.actions = mdp_actions
        self.gamma = 0.95  # discount rate
        self.epsilon = 0.3  # exploration rate
        self.num_iterations = 0
        self.Q = q_init
        self.train_mode = train_mode

    def getAction(self, state):
        self.num_iterations += 1
        if random.random() < self.epsilon:
            return random.choice(self.actions(state))
        else:
            return max((self.Q[str((state, a))], a) for a in self.actions(state))[1]

    def stepsize(self):
        if self.train_mode:
            return 1 / math.sqrt(self.num_iterations)
        else:
            return .5

    def updateQ(self, curr_state, action, reward, nxt_state):
        Q_max = max((self.Q[str((nxt_state, a))], a) for a in self.actions(nxt_state))[0]
        self.Q[str((curr_state, action))] = self.Q[str((curr_state, action))] + self.stepsize() * (
                reward + self.gamma * Q_max - self.Q[str((curr_state, action))])

    def optimalPolicy(self):
        states_actions = [ast.literal_eval(key) for key in self.Q]
        states = [val[0] for val in states_actions]
        policy = {}
        for state in states:
            policy[state] = max((self.Q[str((state, a))], a) for a in self.actions(state))[1]
        return policy


# Simulation
def simulate(load_q_filename=None, save_q_filename=None, sim_student_filename=None, train_mode=True, delta=.001,
             max_iter=100000, verbose=True):
    q_init = util.load_q(load_q_filename)
    sim_student = util.load_student(sim_student_filename)

    mdp = MDP()
    mdp.sim_student = sim_student
    ql = QLearning(mdp.actions, q_init, train_mode)

    Q_old = copy.deepcopy(q_init)
    for key in Q_old:
        Q_old[key] = 10

    episode_rewards = []

    cur_state = mdp.start_state()
    for _ in range(max_iter):
        action = ql.getAction(cur_state)
        nxt_state = mdp.successor(cur_state, action)
        reward = mdp.reward(cur_state, action, nxt_state)
        ql.updateQ(cur_state, action, reward, nxt_state)

        cur_state = nxt_state
        episode_rewards.append(reward)

        if mdp.isEnd(cur_state) or (sum([abs(ql.Q[key] - Q_old[key]) for key in q_init]) < delta and train_mode):
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
    #simulate(sim_student_filename='student_cortney.json')

    Q_table, episode_rewards = simulate(
                                        sim_student_filename='student_cortney.json', train_mode=True)

    #print(Q_table)
    #Q, a = simulate(load_q_filename='student_takara_norm_q.json',
    #                sim_student_filename='student_cortney.json', train_mode=False)
    #Give it a try
    #simulate(load_q_filename='rand_student_q.json', train_mode=False)