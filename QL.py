# observed_states: (num_1_digit, num_2_digit, carry_ops, zero_count, isTrail)
# environment_states: (the actual problem associated with the observed states, number of problems passed, game_status: skip, quit, continue )
# STATE STRUCTURE a tuple consisting of 2 tuples : ( (observed_states), (environment_states) )
import operator
import random
import FeatureExtractor
import time


class Problem:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.operation = 'operation'

class MDP:
    def __init__(self):
        self.temp = None
        self.bins, self.FEATURE_TUPLE_LIMIT = FeatureExtractor.generate_bins_and_constants()
        self.BASE_PROBLEM_KEY = (-1, -1, -1, -1, 'trailFalse')
        self.number_of_passed = 1
        self.game_status = "Cont"

    # Amanda
    def startState(self):
        result = random.choice(self.bins[self.BASE_PROBLEM_KEY])
        start_state = (self.BASE_PROBLEM_KEY, (Problem(result[0], result[1]), self.number_of_passed, self.game_status))
        return start_state

    # Cortney
    # observed_state: (num_1_digit, num_2_digit, carry_ops, zero_count, isTrail)
    def actions(self, state):
        observed_state, environment_state = state
        valid_actions = list()
        stay = tuple([0] * len(observed_state))
        valid_actions.append(stay)
        # if BASE_PROBLEM_KEY the next problem will (deterministically) be a 1-digit + 1-digit (no carry op) question
        if observed_state == self.BASE_PROBLEM_KEY:
            valid_actions.append((2, 2, 1, 1, 'trailFalse'))
            return valid_actions
        # if 'trailTrue' the next problem will (deterministically) be a 2-digit + 1-digit (no carry op) question
        if observed_state[-1] == 'trailTrue':
            valid_actions.append((2, 1, 0, 0, 'trailFalse'))
            return valid_actions
        # otherwise we can try to increment/decrement every feature
        for i in range(len(observed_state)-1):
            for j in [-1, 1]:
                if observed_state[i]+j in self.FEATURE_TUPLE_LIMIT[i]:
                    action = tuple([j if k == i else 0 for k in range(len(observed_state))])
                    valid_actions.append(action)

        return valid_actions

    # Amanda
    def create_problem(self, state, bins):
        try:
            if state in self.bins and len(self.bins[state]) > 0:
                new_problem = random.choice(self.bins[state])
                print(new_problem)
                return Problem(new_problem[0], new_problem[1])
            else:
                new_problem = random.choice(self.bins[self.BASE_PROBLEM_KEY])
                return Problem(new_problem[0], new_problem[1])
        except:
            raise Exception('Cannot find matching tuple in problem bank for next state : ', state)

    def next_state(self, state, action):
        try:
            s1 = state[0:4]
            s2 = action[0:4]
            add_result = list(map(operator.add, s1, s2))
            add_result.append(action[4])
            return tuple(add_result)

        except:
            raise Exception("Operation add failed for next state")

    def compare_tuple(self, a, b):
        for answer in [(a == b) for a, b in zip(a, b)]:
            if not answer:
                return False
        return True

    def successor(self, state, action):
        if type(state) is not tuple or type(action) is not tuple:
            return
        observed_states = state[0]
        if len(observed_states) != len(action):
            return

        new_state = self.next_state(observed_states, action)
        problem = self.create_problem(new_state,self.bins)
        result = (new_state, (problem, state[1][1] + 1, state[1][2]))
        return result

    # Takara
    def reward(self, state):
        reward = 0
        print(state)
        prompt = "{} + {} = \n".format(state[1][0].x, state[1][0].y)
        start_time = time.time()
        val = input(prompt)
        end_time = time.time() - start_time

        if val == 'q':
            self.status = 'Quit'
            return reward

        if val == 'n':
            self.status = 'Next'
            print("Next Question!")
            return reward

        if int(val) == (state[1][0].x + state[1][0].y):
            print("Correct! it took you " + str(int(end_time)) + " seconds!")
            reward = end_time
        else:
            print("Incorrect!")

        return reward

    # Takara
    def isEnd(self, state):
        if self.status == 'Quit' or self.status == 'Next':
            return True
        else:
            return False

class QLearning:
    def __init__(self, mdp_actions, q_init):
        self.actions = mdp_actions
        self.gamma = 0.95  # discount rate
        self.epsilon = 0.3  # exploration rate
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

# #Simulation
# class Simulation(MDP, rl, loadPath=None, savePath=None):
#     def __init__(self, mdp=MDP, rl=QLearning):
#         q_init = collections.defaultdict(lambda: 0) if loadPath is not None else read(loadPath)
#         self.mdp = mdp
#         self.ql = rl(mdp.actions, q_init)
#         self.episode_rewards = []
#         self.quit = False
#
#     def episode(self):
#         self.episode_rewards = []
#         cur_state = mdp.startState()
#
#         while self.ql.isEnd() is None:
#             action = self.ql.getAction(cur_state)
#             reward = self.mdp.reward(cur_state, action)
#             nxt_state = self.mdp.succesor(cur_state, action)
#             self.ql.updateQ(cur_state, action, reward, nxt_state)
#
#             cur_state = nxt_state
#             self.episode_rewards.append(reward)
#
#         if self.ql.quit() is 'Quit':
#             self.quit = True
#
#     def save(self):
#         pass
#
#
# if __name__ == '__main__':
#
#     simulate = Simulation(MDP, QLearning)
#
#     ep_num = 0
#     total_rewards = []
#
#     while self.quit is False | ep_num <= max_episodes:
#         simulate.episode()
#         total_rewards = total_rewards + simulate.episode_rewards
#         ep_num += 1
#
#     #save_stuff
#     simulate.save()
#
#     #stats
#
#     #plotstuff
