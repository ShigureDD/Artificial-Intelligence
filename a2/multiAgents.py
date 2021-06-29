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
        prevFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        foodList = prevFood.asList()
        successorScore = successorGameState.getScore()

        minDistance = min([manhattanDistance(newPos, food) for food in foodList])
        if min(newScaredTimes) <=1:
          successorScore += 1/(minDistance+1)
        else:
          successorScore += (1 + min(newScaredTimes))/(minDistance + 1)

        if newPos == currentGameState.getPacmanPosition():
          successorScore = float("-inf")

        minGhostDistance = float("inf")
        for ghostState in newGhostStates:
          ghostDistance = manhattanDistance(ghostState.getPosition(), newPos)
          if ghostDistance < minGhostDistance:
            minGhostDistance = ghostDistance
          if ghostState.getPosition() == newPos and ghostState.scaredTimer == 0:
            successorScore = float("-inf")
        successorScore -=  1/(minGhostDistance + 1)

        return successorScore
        

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

          gameState.isWin():
            Returns whether or not the game state is a winning state

          gameState.isLose():
            Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def Maximum(state, depth, index):
          if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state)
          v = float('-inf')
          for act in state.getLegalActions(index):
              v = max(v, Minimum(state.generateSuccessor(0, act), depth, 1 ))
          return v

        def Minimum(state, depth, index):
          if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state)
          v = float('inf')
          for act in state.getLegalActions(index):
            if gameState.getNumAgents()==index+1:
              v = min(v, Maximum(state.generateSuccessor(index, act), depth-1, 0))
            else:
              v = min(v, Minimum(state.generateSuccessor(index, act), depth, index + 1))
          return v

        Max = float('-inf')
        direction = Directions.STOP
        for act in gameState.getLegalActions(0):
            MaxAct = Minimum(gameState.generateSuccessor(0, act), self.depth, 1)
            if MaxAct > Max :
              Max,direction  = MaxAct,act
        return direction 


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def Maximum(state, depth, index, alpha, beta):
          if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state)
          v = float('-inf')
          for act in state.getLegalActions(index):
              v = max(v, Minimum(state.generateSuccessor(0, act), depth, 1 , alpha, beta))
              if v > beta:
                return v
              alpha = max(alpha, v)
          return v

        def Minimum(state, depth, index, alpha, beta):
          if state.isWin() or state.isLose() or depth == 0:
              return self.evaluationFunction(state)
          v = float('inf')
          for act in state.getLegalActions(index):
            if gameState.getNumAgents()==index+1:
              v = min(v, Maximum(state.generateSuccessor(index, act), depth-1, 0, alpha, beta))
            else:
              v = min(v, Minimum(state.generateSuccessor(index, act), depth, index + 1, alpha, beta))
            if v < alpha:
              return v
            beta = min(beta, v)
          return v

        Max, alpha, beta = float('-inf'),float('-inf'), float('inf')
        direction = Directions.STOP
        for act in gameState.getLegalActions(0):
          MaxAct = Minimum(gameState.generateSuccessor(0, act), self.depth, 1, alpha, beta)
          if MaxAct>Max:
            Max, direction= MaxAct,act
          if MaxAct > beta:
            return MaxAct
          alpha = max(alpha, MaxAct)

        return direction 
        

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
        def Maximum(state, depth, index):
          if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state)
          v = float('-inf')
          for act in state.getLegalActions(index):
              v = max(v, Minimum(state.generateSuccessor(0, act), depth, 1 ))
          return v

        def Minimum(state, depth, index):
          if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state)
          v = 0
          for act in state.getLegalActions(index):
            if gameState.getNumAgents()==index+1:
              v += Maximum(state.generateSuccessor(index, act), depth-1, 0)
            else:
              v += Minimum(state.generateSuccessor(index, act), depth, index + 1)
          
          return v/len(state.getLegalActions(index))

        Max = float('-inf')
        direction = Directions.STOP
        for act in gameState.getLegalActions(0):
            MaxAct = Minimum(gameState.generateSuccessor(0, act), self.depth, 1)
            if MaxAct>Max:
                Max, direction= MaxAct,act
        return direction 

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    minGhostDistance = float("inf")

    foodList = currentGameState.getFood().asList()
    if len(foodList) == 0:
      return float("inf")

    minDistance = min([manhattanDistance(newPos, food) for food in foodList])
      
    if min(newScaredTimes) == 0:
      score += 3/(minDistance + 1)
    else:
      score += (3 + min(newScaredTimes))/(minDistance + 1)

    capsuleList = currentGameState.getCapsules()
    if len(capsuleList) > 0:
      minDistance = min([manhattanDistance(newPos, food) for food in capsuleList])
      score += 5/(minDistance + 1)

    for ghostState in newGhostStates:
      ghostDistance = manhattanDistance(ghostState.getPosition(), newPos)
      if ghostDistance < minGhostDistance:
        minGhostDistance = ghostDistance
      if ghostState.getPosition() == newPos and ghostState.scaredTimer == 0:
        score -= 5/(minGhostDistance + 1)
    return score
# Abbreviation
better = betterEvaluationFunction

