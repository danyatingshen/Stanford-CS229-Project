# observed_states: (total digits, digit difference, ...... )
# environment_states: (the actual problem associated with the observed states, number of problems passed, game_status: skip, quit, continue )
# STATE STRUCTURE a tuple consisting of 2 tuples : ( (observed_states), (environment_states) )
import operator
import random
import FeatureExtractor
import re


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
        self.game_status = "continue"

    # Amanda
    def startState(self):
        result = random.choice(FeatureExtractor.bins[self.BASE_PROBLEM_KEY])
        return zip(self.BASE_PROBLEM_KEY, (Problem(result[0], result[1]), self.number_of_passed, self.game_status))

    # Cortney
    def actions(self, state):
        observed_state, environment_state = state
        actions = {}
        for i in range(len(observed_state)):
            stay = tuple([0] * len(observed_state))
            actions.add(stay)
            if state < FeatureExtractor.self.MAX_FEATURE_TUPLE:
                increase = tuple(1 if i == j else 0 for j in range(len(observed_state)))
                actions.add(increase)
            if state > FeatureExtractor.self.MIN_FEATURE_TUPLE:
                decrease = tuple(-1 if i == j else 0 for j in range(len(observed_state)))
                actions.add(decrease)
        return actions

    # Amanda
    def create_problem(state, bins):
        try:
            new_problem = random.choice(bins[state])
            return Problem(new_problem[0], new_problem[1])
        except:
            raise Exception('Cannot find matching tuple in problem bank for next state : ', state)

        raise Exception('Cannot find matching tuple in problem bank for next state : ', state)

    def next_state(self, state, action):
        try:
            return tuple(map(operator.add, state, action))
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
        problem = self.create_problem(new_state)
        return zip(new_state, (problem, state[1][1] + 1, state[1][2]))

    # Takara
    def reward(self, state):
        pass

    # Takara
    def isEnd(self, state):
        # next_question

        # end_game

        # return 'Quit'
        return None


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
