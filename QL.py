# observed_states: (num_1_digit, num_2_digit, carry_ops, zero_count, isTrail)
# environment_states: (the actual problem associated with the observed states, number of problems passed, game_status: skip, quit, continue )
# STATE STRUCTURE a tuple consisting of 2 tuples : ( (observed_states), (environment_states) )
import operator
import random
import FeatureExtractor
import time
import collections


class Problem:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.operation = 'operation'

class MDP:
    def __init__(self):
        self.temp = None
        self.bins, self.FEATURE_TUPLE_LIMIT = FeatureExtractor.generate_bins_and_constants()
        self.BASE_PROBLEM_KEY = (-1, -1, -1, -1)
        self.number_of_passed = 1
        self.status = "Cont"

        self.problem = None
    # Amanda
    def startState(self):
        result = random.choice(self.bins[self.BASE_PROBLEM_KEY])
        #start_state = (self.BASE_PROBLEM_KEY, (Problem(result[0], result[1]), self.number_of_passed, self.status))
        start_state = (self.BASE_PROBLEM_KEY)
        self.problem = Problem(result[0], result[1])

        return start_state

    # Cortney
    # observed_state: (num_1_digit, num_2_digit, carry_ops, zero_count, isTrail)
    def actions(self, state):
        observed_state = state#, environment_state = state
        valid_actions = list()
        stay = tuple([0] * len(observed_state))
        valid_actions.append(stay)
        # if BASE_PROBLEM_KEY the next problem will (deterministically) be a 1-digit + 1-digit (no carry op) question
        if observed_state == self.BASE_PROBLEM_KEY:
            valid_actions.append((2, 2, 1, 1))
            return valid_actions
        # otherwise we can try to increment/decrement every feature
        for i in range(len(observed_state)):
            for j in [-1, 1]:
                if observed_state[i] + j in self.FEATURE_TUPLE_LIMIT[i]:
                    action = tuple([j if k == i else 0 for k in range(len(observed_state))])
                    if len(self.bins[self.next_state(observed_state,action)]) > 0:
                        valid_actions.append(action)

        return valid_actions

    # Amanda
    def create_problem(self, state):
        try:
            if state in self.bins and len(self.bins[state]) > 0:
                new_problem = random.choice(self.bins[state])
                #print("Create Problem Successfully!", new_problem)
                return Problem(new_problem[0], new_problem[1])
        except:
            raise Exception('Cannot find matching tuple in problem bank for next state : ', state)

    def next_state(self, state, action):
        try:
            add_result = tuple(map(operator.add, state, action))
            return add_result
        except:
            raise Exception("Operation add failed for next state")

    def compare_tuple(self, a, b):
        for answer in [(a == b) for a, b in zip(a, b)]:
            if not answer:
                return False
        return True

    def succesor(self, state, action):
        if type(state) is not tuple or type(action) is not tuple:
            return
        observed_states = state
        if len(observed_states) != len(action):
            return

        new_state = self.next_state(observed_states, action)
        self.problem = self.create_problem(new_state)
        #result = (new_state, (problem, state[1][1] + 1, state[1][2]))
        result = new_state
        #self.problem = problem
        return result

    # Takara
    def reward(self, state,action,next_state):
        reward = 10
        print(state)
        prompt = "{} + {} = \n".format(self.problem.x, self.problem.y)
        start_time = time.time()
        val = ""
        while val ==  "":
            val = input(prompt)

        end_time = time.time() - start_time

        if val == 'q':
            self.status = 'Quit'
            return reward

        if val == 'n':
            self.status = 'Next'
            print("Next Question!")
            return reward

        if int(val) == (self.problem.x + self.problem.y):
            print("Correct! it took you " + str(int(end_time)) + " seconds!")
            reward = end_time
        else:
            print("Incorrect!")

        return reward

    # Takara
    def isEnd(self, state):
        if self.status == 'Quit': # greater than 10 questions.
            return True
        else:
            return False


class QLearning:
    def __init__(self, mdp_actions, q_init):
        self.actions = mdp_actions
        self.gamma = 0.95  # discount rate
        self.epsilon = 0.4  # exploration rate
        self.numIters = 0
        self.Q = q_init

    def getAction(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions(state))
        else:
            return max((self.Q[(state, a)], a) for a in self.actions(state))[1]

    def stepsize(self):
        return .5

    def updateQ(self, curr_state, action, reward, nxt_state):
        Q_max = max((self.Q[(nxt_state, a)], a) for a in self.actions(nxt_state))[0]
        self.Q[(curr_state, action)] = self.Q[(curr_state, action)] + self.stepsize() * (
                reward + self.gamma * Q_max - self.Q[(curr_state, action)])


#Simulation
def simulate(loadPath=None, savePath=None):

        if loadPath is None:
            q_init = collections.defaultdict(lambda: 0)
        else:
            q_init = collections.defaultdict(lambda: 0)

        mdp = MDP()
        ql = QLearning(mdp.actions, q_init)
        episode_rewards = []

        cur_state = mdp.startState()
        while mdp.isEnd(cur_state) is False:
            action = ql.getAction(cur_state)
            nxt_state = mdp.succesor(cur_state, action)
            reward = mdp.reward(cur_state, action, nxt_state)
            ql.updateQ(cur_state, action, reward, nxt_state)

            cur_state = nxt_state
            episode_rewards.append(reward)

        return ql.Q

if __name__ == '__main__':

    Q_table = simulate()
    print(Q_table)