# -*- coding: utf-8 -*-
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
import Queue

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
    startState = problem.getStartState()
    startNode = (startState, [], 0)

    frontier = util.Stack()
    frontier.push(startNode)
    explored = set()

    while not frontier.isEmpty():
        cur_node = frontier.pop()        # current_what
        if problem.isGoalState(cur_node[0]):
            return cur_node[1]
        if cur_node[0] not in explored:
            explored.add(cur_node[0])
            for isuc in problem.getSuccessors(cur_node[0]):
                suc_state, suc_action, suc_cost = isuc    # successor_what
                new_action = cur_node[1] + [suc_action]
                new_cost = cur_node[2] + suc_cost
                new_node = (suc_state, new_action, new_cost)
                frontier.push(new_node)
    return []
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    startState = problem.getStartState()
    startNode = (startState, [], 0)

    frontier = util.Queue()
    frontier.push(startNode)
    explored = set()

    while not frontier.isEmpty():
        cur_node= frontier.pop()  # current_what
        if problem.isGoalState(cur_node[0]):
            return cur_node[1]
        if cur_node[0] not in explored:
            explored.add(cur_node[0])
            for isuc in problem.getSuccessors(cur_node[0]):
                suc_state, suc_action, suc_cost = isuc  # successor_what
                new_action = cur_node[1] + [suc_action]
                new_cost = cur_node[2] + suc_cost
                new_node = (suc_state, new_action, new_cost)
                frontier.push(new_node)
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    class Node:
        def __init__(self, state, action, g):
            self.state = state
            self.action = action
            self.cost = g

        def get_g(self):
            return self.cost

    startState = problem.getStartState()
    startNode = Node(startState, [], 0)

    frontier = Queue.PriorityQueue()
    frontier.put((startNode.get_g(), startNode))
    explored = set()

    while not frontier.empty():
        (cur_g, cur_node) = frontier.get()        # current_what
        if problem.isGoalState(cur_node.state):
            return cur_node.action
        if cur_node.state not in explored:
            explored.add(tuple(cur_node.state))
            for isuc in problem.getSuccessors(cur_node.state):
                suc_state, suc_action, suc_cost = isuc    # successor_what
                new_action = cur_node.action + [suc_action]
                new_cost = cur_node.cost + suc_cost
                new_node = Node(suc_state, new_action, new_cost)
                frontier.put((new_node.get_g(), new_node))
    return []

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
    def f(node):
        g = node[2]
        h = heuristic(node[0], problem)
        return g + h

    startState = problem.getStartState()
    startNode = (startState, [], 0)

    frontier = Queue.PriorityQueue()
    frontier.put((f(startNode), startNode))
    explored = set()

    while not frontier.empty():
        (cur_f, cur_node) = frontier.get()        # current_what
        if problem.isGoalState(cur_node[0]):
            return cur_node[1]
        if len(explored):
            tmp = explored
            # print(tmp.pop())
        if cur_node[0] not in explored:
            explored.add(cur_node[0])
            for isuc in problem.getSuccessors(cur_node[0]):
                suc_state, suc_action, suc_cost = isuc          # successor_what
                new_action = cur_node[1] + [suc_action]
                new_cost = cur_node[2] + suc_cost
                new_node = (suc_state, new_action, new_cost)
                frontier.put((f(new_node), new_node))
    return []

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
