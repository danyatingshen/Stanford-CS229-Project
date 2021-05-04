# obseved_states: (total digits, digit difference, ...... )
# environment_states: (the actual problem associated with the observed states, number of problems passed, game_status: skip, quit, continue )
# STATE STRUCTURE a tuple consisting of 2 tuples : ( (observed_states), (environement_states) )
import operator
import random
import FeatureExtractor

class Problem:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.operation = 'operation'
        self.bins, self.MAX_FEATURE_TUPLE, self.MIN_FEATURE_TUPLE = FeatureExtractor.generate_bins_and_constants()
        self.BASE_PROBLEM_KEY = (1, 3, 0, 1, 'trailFalse')

class MDP:
    def __init__(self):
        self.temp = None

    # Amanda
    def startState(self):
        result = random.choice(FeatureExtractor.self.bins[self.BASE_PROBLEM_KEY])
        return Problem(result[0], result[1])

    # Cortney
    def actions(self, state):
        actions = {}
        for i in range(len(state[0])):
            increase = tuple(1 if i == j else 0 for j in range(len(state[0])))
            decrease = tuple(-1 if i == j else 0 for j in range(len(state[0])))
            actions.add((increase, state[1]))
            actions.add((decrease, state[1]))
        return actions

    # Amanda
    def create_problem(self,state):
        with open("problemBank", "r") as param_file:
            raw = param_file.read()
            lines = re.findall(r'\(.*?\)', raw)
            if lines[0] == str(state):
                problem_lst = lines[1:]
                result = random.choice(problem_lst)
                return Problem(result[1], result[4])

        raise Exception('Cannot find matching tuple in problem bank for next state : ', state)

    def next_sate(self,state, action):
        try:
            return tuple(map(operator.add, state, action))
        except:
            print("exception next_sate")

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

        new_state = self.next_sate(observed_states, action)
        problem = self.create_problem(new_state)
        return new_state, problem



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
