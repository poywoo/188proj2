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
        newPos = successorGameState.getPacmanPosition() #(x,y)
        newFood = successorGameState.getFood() #boolean
        newGhostStates = successorGameState.getGhostStates() #game.AgentState instace @addr
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates] #[int]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        if successorGameState.isWin(): 
          return 10000
        ghostPos = currentGameState.getGhostPositions()
        mdFromGhost = util.manhattanDistance(newPos, ghostPos[0])
        
        if mdFromGhost < 10:
          if newScaredTimes < 5:
            score -= 5*mdFromGhost
          else:
            score += mdFromGhost
  
        foodList = newFood.asList()
        minimumDis = util.manhattanDistance(newPos, foodList[0]) + 1
        for potentialTarget in foodList:
            distance = util.manhattanDistance(newPos, potentialTarget)
            if distance < minimumDis:
                minimumDis = distance
        score += 15/minimumDis
        
        if successorGameState.getNumFood() < currentGameState.getNumFood(): 
          score += 100
        powerPellet = currentGameState.getCapsules()
        if newPos in powerPellet:
          score += 150
        if action == Directions.STOP:
          score -= 10

        return score

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
        
        # def maxValue(gameState, depth, totalGhost):
        #   if gameState.isWin() or gameState.isLose() or depth == 0:
        #     return self.evaluationFunction(gameState)
        #   v = float("-inf")
        #   legalActions = gameState.getLegalActions(0)
        #   for action in legalActions:
        #     successor = gameState.generateSuccessor(0, action) 
        #     v = max(v, minValue(successor, depth, 1, totalGhost))
        #   return v
    
        # def minValue(gameState, depth, ghostIndex, totalGhost):
        #   if gameState.isWin() or gameState.isLose() or depth == 0:
        #     return self.evaluationFunction(gameState)
        #   v = float("inf")
        #   legalActions = gameState.getLegalActions(ghostIndex)
        #   if ghostIndex == totalGhost:
        #     for action in legalActions:
        #       successor = gameState.generateSuccessor(ghostIndex, action)
        #       v = min(v, maxValue(successor, depth-1 , totalGhost))
        #   else:
        #     for action in legalActions:
        #       successor = gameState.generateSuccessor(ghostIndex, action)
        #       v = min(v, minValue(successor, depth, ghostIndex+1, totalGhost))
        #   return v
        

        # nextAction = Directions.STOP
        # v = float("-inf")
        # legalActions = gameState.getLegalActions(0)
        # for action in legalActions:
        #   successor = gameState.generateSuccessor(0, action)
        #   newValue = max(v, minValue(successor, self.depth, 1, gameState.getNumAgents()-1))
        #   if newValue > v:
        #     v = newValue
        #     nextAction = action
        # return nextAction
        def maxValue(gameState, depth, totalGhost):
          if gameState.isWin() or gameState.isLose() or depth == 0:
            return [self.evaluationFunction(gameState), Directions.STOP]
          v = float("-inf")
          pair = []
          legalActions = gameState.getLegalActions(0)
          for action in legalActions:
            successor = gameState.generateSuccessor(0, action) 
            newValue = minValue(successor, depth, 1, totalGhost)
            if newValue[0] > v:
              v = newValue[0]
              pair = [v, action]
          return pair
    
        def minValue(gameState, depth, ghostIndex, totalGhost):
          if gameState.isWin() or gameState.isLose() or depth == 0:
            return [self.evaluationFunction(gameState), Directions.STOP]
          v = float("inf")
          pair = []
          legalActions = gameState.getLegalActions(ghostIndex)
          if ghostIndex == totalGhost:
            for action in legalActions:
              successor = gameState.generateSuccessor(ghostIndex, action)
              newValue = maxValue(successor, depth-1 , totalGhost)
              if newValue[0] < v:
                v = newValue[0]
                pair = [v, action]
          else:
            for action in legalActions:
              successor = gameState.generateSuccessor(ghostIndex, action)
              newValue = minValue(successor, depth, ghostIndex+1, totalGhost)
              if newValue[0] < v:
                v = newValue[0]
                pair = [v, action]
          return pair
        
        return maxValue(gameState, self.depth, gameState.getNumAgents()-1)[1]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # def maxValue(gameState, depth, totalGhost, alpha, beta):
        #   if gameState.isWin() or gameState.isLose() or depth == 0:
        #     return self.evaluationFunction(gameState)
        #   v = float("-inf")
        #   legalActions = gameState.getLegalActions(0)
        #   for action in legalActions:
        #     successor = gameState.generateSuccessor(0, action)
        #     v = max(v, minValue(successor, depth, 1, totalGhost, alpha, beta))
        #     if v > beta:
        #       return v
        #     alpha = max(alpha, v)
        #   return v
    
        # def minValue(gameState, depth, ghostIndex, totalGhost, alpha, beta):
        #   if gameState.isWin() or gameState.isLose() or depth == 0:
        #     return self.evaluationFunction(gameState)
        #   v = float("inf")
        #   legalActions = gameState.getLegalActions(ghostIndex)
        #   if ghostIndex == totalGhost:
        #     for action in legalActions:
        #       successor = gameState.generateSuccessor(ghostIndex, action)
        #       v = min(v, maxValue(successor, depth-1 , totalGhost, alpha, beta))
        #       if v < alpha:
        #         return v
        #       beta = min(beta, v)
        #   else:
        #     for action in legalActions:
        #       successor = gameState.generateSuccessor(ghostIndex, action)
        #       v = min(v, minValue(successor, depth, ghostIndex+1, totalGhost, alpha, beta))
        #       if v < alpha:
        #         return v
        #       beta = min(beta, v)
        #   return v
        

        # nextAction = Directions.STOP
        # v = float("-inf")
        # alpha = float("-inf")
        # beta = float("inf")
        # legalActions = gameState.getLegalActions(0)
        # for action in legalActions:
        #   successor = gameState.generateSuccessor(0, action)
        #   newValue = max(v, minValue(successor, self.depth, 1, gameState.getNumAgents()-1, alpha, beta))
        #   if newValue > v:
        #     v = newValue
        #     nextAction = action
        #   if newValue > beta: 
        #     return nextAction
        #   alpha = max(alpha, v)
        # return nextAction
        def maxValue(gameState, depth, totalGhost, alpha, beta):
          if gameState.isWin() or gameState.isLose() or depth == 0:
            return [self.evaluationFunction(gameState), Directions.STOP]
          v = float("-inf")
          pair = []
          legalActions = gameState.getLegalActions(0)
          for action in legalActions:
            successor = gameState.generateSuccessor(0, action) 
            newValue = minValue(successor, depth, 1, totalGhost, alpha, beta)
            if newValue[0] > v:
              v = newValue[0]
              pair = [v, action]
              if v > beta:
                return pair
              alpha = max(alpha, v)
          return pair
    
        def minValue(gameState, depth, ghostIndex, totalGhost, alpha, beta):
          if gameState.isWin() or gameState.isLose() or depth == 0:
            return [self.evaluationFunction(gameState), Directions.STOP]
          v = float("inf")
          pair = []
          legalActions = gameState.getLegalActions(ghostIndex)
          if ghostIndex == totalGhost:
            for action in legalActions:
              successor = gameState.generateSuccessor(ghostIndex, action)
              newValue = maxValue(successor, depth-1 , totalGhost, alpha, beta)
              if newValue[0] < v:
                v = newValue[0]
                pair = [v, action]
              if v < alpha:
                return pair
              beta = min(beta, v)
          else:
            for action in legalActions:
              successor = gameState.generateSuccessor(ghostIndex, action)
              newValue = minValue(successor, depth, ghostIndex+1, totalGhost, alpha, beta)
              if newValue[0] < v:
                v = newValue[0]
                pair = [v, action]
              if v < alpha:
                return pair
              beta = min(beta, v)
          return pair
        
        alpha = float("-inf")
        beta = float("inf")
        return maxValue(gameState, self.depth, gameState.getNumAgents()-1, alpha, beta)[1]

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
        def maxValue(gameState, depth, totalGhost):
          if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
          v = float("-inf")
          legalActions = gameState.getLegalActions(0)
          for action in legalActions:
            successor = gameState.generateSuccessor(0, action)
            v = max(v, expValue(successor, depth, 1, totalGhost))
          return v

        def expValue(gameState, depth, ghostIndex, totalGhost):
          if gameState.isWin() or gameState.isLose() or depth == 0:
            return self.evaluationFunction(gameState)
          v = 0.0
          legalActions = gameState.getLegalActions(ghostIndex)
          if ghostIndex == totalGhost:
            for action in legalActions:
              successor = gameState.generateSuccessor(ghostIndex, action)
              v += maxValue(successor, depth-1 , totalGhost)
          else:
            for action in legalActions:
              successor = gameState.generateSuccessor(ghostIndex, action)
              v += expValue(successor, depth, ghostIndex+1, totalGhost)
          return v/float(len(legalActions))

        nextAction = Directions.STOP
        v = float("-inf")
        legalActions = gameState.getLegalActions(0)
        for action in legalActions:
          successor = gameState.generateSuccessor(0, action)
          newValue = max(v, expValue(successor, self.depth, 1, gameState.getNumAgents()-1))
          if newValue > v:
            v = newValue
            nextAction = action
        return nextAction
        # def maxValue(gameState, depth, totalGhost):
        #   if gameState.isWin() or gameState.isLose() or depth == 0:
        #     return [self.evaluationFunction(gameState), Directions.STOP]
        #   v = float("-inf")
        #   pair = []
        #   legalActions = gameState.getLegalActions(0)
        #   for action in legalActions:
        #     successor = gameState.generateSuccessor(0, action) 
        #     newValue = expValue(successor, depth, 1, totalGhost)
        #     if newValue > v:
        #       v = newValue
        #       pair = [v, action]
        #   return pair

        # def expValue(gameState, depth, ghostIndex, totalGhost):
        #   if gameState.isWin() or gameState.isLose() or depth == 0:
        #     return self.evaluationFunction(gameState)
        #   v = 0.0
        #   legalActions = gameState.getLegalActions(ghostIndex)
        #   if ghostIndex == totalGhost:
        #     for action in legalActions:
        #       successor = gameState.generateSuccessor(ghostIndex, action)
        #       v += maxValue(successor, depth-1 , totalGhost)[0]
        #   else:
        #     for action in legalActions:
        #       successor = gameState.generateSuccessor(ghostIndex, action)
        #       v += expValue(successor, depth, ghostIndex+1, totalGhost)
        #   return v/float(len(legalActions))

        # return maxValue(gameState, self.depth, gameState.getNumAgents()-1)[1]


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: 
      In my evaluation function, I penalized the game state for having a large amout of 
      food left on the board, especially if a ghost was far away. If a ghost was close, 
      then I prioritized staying far from the ghost. I gave additional points for eating
      the power pellets but that was also not a priority.
    """
    "*** YOUR CODE HERE ***"

    currPos = currentGameState.getPacmanPosition() #(x,y)
    currFood = currentGameState.getFood() #boolean
    currGhostStates = currentGameState.getGhostStates() #game.AgentState instace @addr
    currScaredTimes = [ghostState.scaredTimer for ghostState in currGhostStates] #[int]

    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    if currentGameState.isWin(): 
      return float("inf")
    if currentGameState.isLose(): 
      return float("-inf")
    
    dis  = float("inf")
    ghostPos = currentGameState.getGhostPositions()
    for ghost in ghostPos:
      mdFromGhost = util.manhattanDistance(currPos, ghost)
      dis = min(mdFromGhost, dis)

    foodList = currFood.asList()
    minimumDis = util.manhattanDistance(currPos, foodList[0]) + 1
    for potentialTarget in foodList:
        distance = util.manhattanDistance(currPos, potentialTarget)
        if distance < minimumDis:
            minimumDis = distance
    score += 15.0/float(minimumDis)

    if dis < 5 and currScaredTimes < 5:
      score -= 5*dis
    if dis < 5 and currScaredTimes > 5:
      score += dis
    if dis > 5 and len(foodList) > 0:
      score -= 5*len(foodList)

    powerPellet = currentGameState.getCapsules()
    score -= 2*len(powerPellet)
    
    #  score += 10.0/float(len(powerPellet))
    # if len(foodList) > 0:
    #   score += 20.0/float(len(foodList))

    return score


# Abbreviation
better = betterEvaluationFunction



