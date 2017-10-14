# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


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

        for i in range(0, self.iterations):
          counter_values = util.Counter()
          
          for state in self.mdp.getStates():
            
            if self.mdp.isTerminal(state):
              counter_values[state] = 0
            
            else:
              maxval = float("-inf")
            
              for action in self.mdp.getPossibleActions(state):
                qvalue = self.computeQValueFromValues(state,action)
                
                if maxval < qvalue:
                    maxval = qvalue

              counter_values[state] = maxval

          self.values = counter_values

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
        transition_tuples = self.mdp.getTransitionStatesAndProbs(state, action)
        q_val = 0

        for nextState, transition_prob in transition_tuples:
            reward = self.mdp.getReward(state, action, nextState)
            # using equation from lecture: Q(s,a) = sum(T * (R + disc*V))
            q_val += transition_prob * (reward + (self.discount * self.values[nextState]))

        return q_val
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        poss_actions = self.mdp.getPossibleActions(state)

        if len(poss_actions) == 0:
            return None
       
        value = float("-inf")
        policy = None

        for action in poss_actions:
            if self.computeQValueFromValues(state, action) >= value:
                value = self.computeQValueFromValues(state, action)
                policy = action

        return policy

        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
