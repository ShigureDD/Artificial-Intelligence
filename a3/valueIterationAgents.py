import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        
        
        for i in range(0, self.iterations):
            new_value = util.Counter()

            for state in states:
                actions = self.mdp.getPossibleActions(state)
                Q_star = float("-inf")

                for action in actions:
                    Q = self.getQValue(state,action)
                    if Q > Q_star:
                        Q_star = Q

                if self.mdp.isTerminal(state) or len(actions) == 0:
                    new_value[state] = 0
                else:
                    new_value[state] = Q_star

            self.values = new_value


    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        next_transition_states = self.mdp.getTransitionStatesAndProbs(state,action)
        Q_sum = 0

        for next_transition_state in next_transition_states:
            reward = self.mdp.getReward( state, action, next_transition_state[0] )
            Q = next_transition_state[1] * (reward + self.discount * self.getValue(next_transition_state[0]) )
            Q_sum += Q

        return Q_sum

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state) or len(self.mdp.getPossibleActions(state)) == 0:
            return None

        Q_star = float("-inf")
        actions = self.mdp.getPossibleActions(state)
        max_action = actions[0]

        for action in actions:
            Q = self.getQValue(state,action)

            if Q > Q_star:
                Q_star = Q
                max_action = action

        return max_action

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
