


#obseved_states: (total digits, digit difference, ...... )
#environment_states: (the actual problem associated with the observed states, number of problems passed, game_status: skip, quit, continue )
#STATE STRUCTURE a tuple consisting of 2 tuples : ( (observed_states), (environement_states) )

class MDP:
    def __init__(self):
        self.temp = None

    #Amanda
    def startState(self):
        pass

    #Cortney
    def actions(self, state):
        actions = {}
        for i in range(len(state[0])):
            increase = tuple(1 if i == j else 0 for j in range(len(state[0])))
            decrease = tuple(-1 if i == j else 0 for j in range(len(state[0])))
            actions.add((increase), state[1])
            actions.add((decrease), state[1])
        return actions


    #Amanda
    def successor(self, state, action):
        pass

    #Takara
    def reward(self, state):
        pass

    #Takara
    def isEnd(self, state):
        #next_question

        #end_game

        #return 'Quit'
        return None


class QLearning:
    def __init__(self, mdp_actions, q_init):
        self.actions = mdp_actions
        self.gamma = 0.95  # discount rate
        self.epsilon = 0.3 # exploration rate
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
        self.Q[(curr_state, action)] = self.Q[(curr_state, action)] + self.stepsize() * (reward + self.gamma * Q_max - self.Q[(curr_state, action)])


#Simulation
class Simulation(mdp, rl, loadPath=None, savePath=None):
    def __init__(self, mdp=MDP, rl=QLearning):
        q_init = collections.defaultdict(lambda: 0) if loadPath is not None else read(loadPath)
        self.mdp = mdp
        self.ql = rl(mdp.actions, q_init)
        self.episode_rewards = []
        self.quit = False

    def episode(self):
        self.episode_rewards = []
        cur_state = mdp.startState()

        while self.ql.isEnd() is None:
            action = self.ql.getAction(cur_state)
            reward = self.mdp.reward(cur_state, action)
            nxt_state = self.mdp.succesor(cur_state, action)
            self.ql.updateQ(cur_state, action, reward, nxt_state)

            cur_state = nxt_state
            self.episode_rewards.append(reward)

        if self.ql.quit() is 'Quit':
            self.quit = True

    def save(self):
        pass


if __name__ == '__main__':

    simulate = Simulation(MDP, QLearning)

    ep_num = 0
    total_rewards = []

    while self.quit is False | ep_num <= max_episodes:
        simulate.episode()
        total_rewards = total_rewards + simulate.episode_rewards
        ep_num += 1

    #save_stuff
    simulate.save()

    #stats

    #plotstuff


