# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

## generic search alg for dfs, bfs, ucs
def genericSearch(problem, alg):
    ## set up algorithm specific data structure, pop order will change 
    dStruct = {'dfs': util.Stack(), 'bfs': util.Queue(), 'ucs': util.PriorityQueue()}
    startnode = problem.getStartState()
    
    explored = set() # keep explored nodes in a set
    fringe = dStruct[alg] # fringe should be handled with struct specific to the algorithm
    if alg == 'ucs':
        fringe.push((startnode, [], 0), 0)
    else:
        fringe.push((startnode, [], 0))
    
    while not fringe.isEmpty():
        node, path, cost = fringe.pop()
        if problem.isGoalState(node):
            return path
        if node not in explored:
            ## explore it
            explored.add(node)
            ## get children of nodes and add to fringe
            for child_node, child_path, child_cost in problem.getSuccessors(node):
                ##i f child_node not in explored:
                    if alg == 'ucs':
                        fringe.push((child_node, path + [child_path], child_cost + cost), child_cost + cost)
                    else:
                        fringe.push((child_node, path + [child_path], child_cost))
                    
            
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    return genericSearch(problem, alg='dfs')
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    return genericSearch(problem, alg='bfs')
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    return genericSearch(problem, alg='ucs')
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    ## similar to generic search above but with added Heuristic
    startnode = problem.getStartState()
    
    explored = set()
    fringe = util.PriorityQueue()
    fringe.push((startnode, [], 0), 0)

    while not fringe.isEmpty():
        node, path, cost = fringe.pop()
        if problem.isGoalState(node):
            return path
        if node not in explored:
            ## explore it
            explored.add(node)
            ## get children of nodes and add to fringe
            for child_node, child_path, child_cost in problem.getSuccessors(node):
                ##if child_node not in explored:
                heur_cost = heuristic(child_node, problem)
                priority_cost = child_cost + cost
                fringe.push((child_node, path + [child_path], priority_cost), priority_cost + heur_cost)
                    
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
