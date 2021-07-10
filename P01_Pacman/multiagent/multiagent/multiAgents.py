# -*- coding=utf-8 -*-
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
import sys
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
        """
        if successorGameState.isWin():
            return sys.maxint
        if successorGameState.isLose():
            return -sys.maxint

        ghostPositions = [ghostState.getPosition(
        ) for ghostState in newGhostStates if ghostState.scaredTimer == 0]
        if ghostPositions:
            closestGhost = min([util.manhattanDistance(
                newPos, ghostPos) for ghostPos in ghostPositions])
            if closestGhost == 0:
                return -sys.maxint
        else:
            return sys.maxint

        closestFood = min([util.manhattanDistance(newPos, foodPos)
                           for foodPos in newFood.asList()])
        """
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

    def minimax(self, gameState, depth, agent):         # 返回值为（评分，动作）
        action = gameState.getLegalActions(agent)
        if depth > self.depth or len(action) == 0 or gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), Directions.STOP
        if agent == 0:                 #max
            max_value = -float('Inf')
            max_action = Directions.STOP
            for a in action:
                state = gameState.generateSuccessor(agent, a)
                new_score = self.minimax(state, depth, 1)[0]
                if new_score > max_value:
                    max_value = new_score
                    max_action = a
            return max_value, max_action
        else:
            min_value = float('Inf')
            for a in action:
                state = gameState.generateSuccessor(agent, a)
                if agent != gameState.getNumAgents()-1:
                    new_score = self.minimax(state, depth, agent+1)[0]
                else:
                    new_score = self.minimax(state, depth+1, 0)[0]
                min_action = Directions.STOP
                if new_score < min_value:
                    min_value = new_score
                    min_action = a
            return min_value, min_action




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
        optimalscore, optimalaction = self.minimax(gameState, 1, 0)
        return optimalaction

        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        def maxvalue(state, alpha, beta, depth):
            if state.isWin() or state.isLose() or depth >= self.depth:
                return self.evaluationFunction(state), Directions.STOP
            max_score = -float('inf')
            action = Directions.STOP
            for a in state.getLegalActions(0):
                tempbeta = minvalue(state.generateSuccessor(0, a), alpha, beta, depth, 1)[0]
                if tempbeta > max_score:
                    max_score = tempbeta
                    action = a
                if max_score > beta:
                    return max_score, action        # 剪枝
                alpha = max(alpha, max_score)
            return max_score, action

        def minvalue(state, alpha, beta, depth, num):
            if state.isWin() or state.isLose():       #min need pay attention to depth
                return self.evaluationFunction(state), Directions.STOP
            min_score = float('inf')
            action = Directions.STOP
            if num != gameState.getNumAgents()-1:
                for a in state.getLegalActions(num):
                    tempalpha = minvalue(state.generateSuccessor(num, a), alpha, beta, depth, num+1)[0]
                    if tempalpha < min_score:
                        min_score = tempalpha
                        action = a
                    if min_score < alpha:
                        return min_score, action
                    beta = min(beta, min_score)
            else:
                for a in state.getLegalActions(num):
                    tempalpha = maxvalue(state.generateSuccessor(num, a), alpha, beta, depth+1)[0]
                    if tempalpha < min_score:
                        min_score = tempalpha
                        action = a
                    if min_score < alpha:
                        return min_score, action
                    beta = min(beta, min_score)
            return min_score, action

        optimalscore, optimalaction = maxvalue(gameState, float('-Inf'), float('Inf'), 0)
        return optimalaction


        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
