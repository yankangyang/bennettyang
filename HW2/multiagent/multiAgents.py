#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def value(self, gameState, agentIndex, currentDepth): 
        # everytime when value() is called, we check if we need to reset 
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0 # reset agents
            currentDepth += 1 # update depth˙

        # evaluate if in terminal state
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, currentDepth)
        else:
            return self.minValue(gameState, agentIndex, currentDepth)
        
    def minValue(self, gameState, agentIndex, currentDepth):
        # (VALUE, ACTION) tuples
        v = (float("inf"), "undet") 
        
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

        # list of legal actions (minus stops)
        legalActions = [action for action in gameState.getLegalActions(agentIndex) if action != "Stop"]

        for action in legalActions:
            temp = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, currentDepth)
            if type(temp) is tuple:
                temp = temp[0] 

            if temp < v[0]:
              v = (temp, action)
        return v

    def maxValue(self, gameState, agentIndex, currentDepth):
        v = (float("-inf"), "undet")
        
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

        legalActions = [action for action in gameState.getLegalActions(agentIndex) if action != "Stop"]

        for action in legalActions:
            temp = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, currentDepth)
            if type(temp) is tuple:
                temp = temp[0] 

            if temp > v[0]:
              v = (temp, action)

        return v

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        currentDepth = 0
        agentIndex = 0
        val = self.value(gameState, agentIndex, currentDepth)
        return val[1] # return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def value(self, gameState, agentIndex, currentDepth, alpha, beta): 
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0 # reset agents
            currentDepth += 1 # update depth

        # evaluate if in terminal state
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, currentDepth, alpha, beta)
        else:
            return self.minValue(gameState, agentIndex, currentDepth, alpha, beta)
        
    def minValue(self, gameState, agentIndex, currentDepth, alpha, beta):
        v = (float("inf"), "undet") 
        
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

        # list of legal actions
        legalActions = [action for action in gameState.getLegalActions(agentIndex) if action != "Stop"]

        for action in legalActions:
            temp = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, currentDepth, alpha, beta)
            if type(temp) is tuple:
                temp = temp[0] 

            if temp < v[0]:
              v = (temp, action)

            if v[0] < alpha: # hard inequalities: piazza question
                return v

            beta = min(beta, v[0])

        return v

    def maxValue(self, gameState, agentIndex, currentDepth, alpha, beta):
        v = (float("-inf"), "undet")
        
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

        legalActions = [action for action in gameState.getLegalActions(agentIndex) if action != "Stop"]

        for action in legalActions:
            temp = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, currentDepth, alpha, beta)
            if type(temp) is tuple:
                temp = temp[0] 

            if temp > v[0]:
              v = (temp, action)

            if v[0] > beta: # hard inequalities: piazza question
                return v
            alpha = max(alpha, v[0])
        return v

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = float("-inf")
        beta = float("inf")
        currentDepth = 0
        agentIndex = 0
        val = self.value(gameState, agentIndex, currentDepth, alpha, beta)
        return val[1] # return action

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def value(self, gameState, agentIndex, currentDepth): 
        if agentIndex >= gameState.getNumAgents():
            agentIndex = 0 # reset agents
            currentDepth += 1 # update depth

        # evaluate if in terminal state
        if currentDepth == self.depth or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, currentDepth)
        else:
            return self.expectedValue(gameState, agentIndex, currentDepth)
        
    def expectedValue(self, gameState, agentIndex, currentDepth):
        # tuples can't be modified so do it in a list
        v = [0, "undet"]
        
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

        # list of legal actions
        legalActions = [action for action in gameState.getLegalActions(agentIndex) if action != "Stop"]

        p = 1.0/len(legalActions) 
        
        for action in legalActions:
            temp = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, currentDepth)
            if type(temp) is tuple:
                temp = temp[0] 

            v[0] += p * temp
            v[1] = action

        return (v[0], v[1]) # return as tuple so you can you previous functions

    def maxValue(self, gameState, agentIndex, currentDepth):
        v = (float("-inf"), "undet")
        
        if not gameState.getLegalActions(agentIndex):
            return self.evaluationFunction(gameState)

        legalActions = [action for action in gameState.getLegalActions(agentIndex) if action != "Stop"]

        for action in legalActions:
            temp = self.value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, currentDepth)
            if type(temp) is tuple:
                temp = temp[0] 

            if temp > v[0]:
              v = (temp, action)
        
        return v

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        currentDepth = 0
        agentIndex = 0
        val = self.value(gameState, agentIndex, currentDepth)
        return val[1] # return action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

