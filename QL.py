# observed_states: (num_1_digit, num_2_digit, carry_ops, zero_count, isTrail)
# environment_states: (the actual problem associated with the observed states, number of problems passed, game_status: skip, quit, continue )
# STATE STRUCTURE a tuple consisting of 2 tuples : ( (observed_states), (environment_states) )
import operator
import random
import time
import collections
import ujson
import pprint
import util
import math

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

        #if self.sim_student is not None:
        #    reward = util.students(self.sim_student, self.problem[0], self.problem[1])
        #    return reward

        val, nxt_state_response_time = util.usr_input(self.problem)
        reward = nxt_state_response_time - self.curr_state_response_time

        self.curr_state_response_time = nxt_state_response_time

        if val == 'q':
            self.status = 'Quit'
            return 0

        if val == 'n':
            self.status = 'Next'
            print("Next Question!")
            reward - abs(reward)

        if int(val) == (self.problem[0] + self.problem[1]):
            print("Correct! it took you " + str(int(reward)) + " seconds longer than the last problem!")
            reward = reward
        else:
            print("Incorrect!it took you " + str(int(reward)) + " seconds longer than the last problem!")
            reward = -abs(reward)

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
            return 1/math.sqrt(self.num_iterations)
        else:
            return .5

    def updateQ(self, curr_state, action, reward, nxt_state):
        Q_max = max((self.Q[str((nxt_state, a))], a) for a in self.actions(nxt_state))[0]
        self.Q[str((curr_state, action))] = self.Q[str((curr_state, action))] + self.stepsize() * (
                reward + self.gamma * Q_max - self.Q[str((curr_state, action))])


# Simulation
def simulate(load_q_filename=None, save_q_filename=None, sim_student_filename=None, train_mode=True, max_iter=10000):
    q_init = util.load_q(load_q_filename)
    sim_student = util.load_student(sim_student_filename)

    mdp = MDP()
    mdp.sim_student = sim_student

    ql = QLearning(mdp.actions, q_init, train_mode)

    episode_rewards = []
    cur_state = mdp.start_state()
    for _ in range(max_iter):

        action = ql.getAction(cur_state)
        nxt_state = mdp.successor(cur_state, action)
        reward = mdp.reward(cur_state, action, nxt_state)
        ql.updateQ(cur_state, action, reward, nxt_state)

        cur_state = nxt_state
        episode_rewards.append(reward)

        if mdp.isEnd(cur_state):
            break

    util.save_q(save_q_filename, ql.Q)

    return ql.Q


if __name__ == '__main__':
    #Q_table = simulate(save_q_filename='q_test.json')
    Q_table = simulate(load_q_filename='q_test.json')

    pprint.pprint(Q_table, width=1)
