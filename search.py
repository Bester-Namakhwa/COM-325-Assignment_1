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
from util import PriorityQueue

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
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    myStack, visited, path = util.Stack(), [], []

    # Firstly checking if start state is goal state #
    if problem.isGoalState(problem.getStartState()):
        return []

    # Start from the beginning and find a path, which is currently emputy
    myStack.push((problem.getStartState(), []))

    while (True):

        # path not found
        if myStack.isEmpty():
            return []

        """Get informations of current state"""
        xy, path = myStack.pop()  # Take position and path
        visited.append(xy)

        """Terminate condition: reach goal"""
        if problem.isGoalState(xy):
            return path

        # push new states in stack and find their path
        if problem.getSuccessors(xy):
            for item in problem.getSuccessors(xy):
                if item[0] not in visited:
                    newPath = path + [item[1]]  # new path
                    myStack.push((item[0], newPath))


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #  util.raiseNotDefined()

    bfsQueue, visited = util.Queue(), []

    startNode = (problem.getStartState(), [])
    bfsQueue.push(startNode)
    while not bfsQueue.isEmpty():
        fd = bfsQueue.pop()
        position = fd[0]
        path = fd[1]

        if position not in visited:
            visited.append(position)
            if problem.isGoalState(position):
                return path

            for suc in list(problem.getSuccessors(position)):
                if suc[0] not in visited:
                    bfsQueue.push((suc[0], path + [suc[1]]))
    return []


def uniformCostSearch(problem):
    """Search the node of least total cost first."""

    "*** YOUR CODE HERE ***"
    #  util.raiseNotDefined()
    from util import PriorityQueue

    # queueXY: ((x,y),[path],priority) #
    queue = PriorityQueue()

    visited = []  # Visited states
    path = []  # Every state keeps it's path from the starting state

    # Check if initial state is goal state #
    if problem.isGoalState(problem.getStartState()):
        return []

    # Start from the beginning and find a solution, path is empty list #
    # with the cheapest priority                                       #
    queue.push((problem.getStartState(), []), 0)

    while (True):

        # Terminate condition: can't find solution #
        if queue.isEmpty():
            return []

        # Get informations of current state #
        point, path = queue.pop()  # Take position and path
        visited.append(point)

        # This only works for autograder    #
        # In lectures we check if a state is a goal when we find successors #

        # Terminate condition: reach goal #
        if problem.isGoalState(point):
            return path

        # Get successors of current state #
        successor = problem.getSuccessors(point)

        # Add new states in queue and fix their path #
        if successor:
            for item in successor:
                if item[0] not in visited and (item[0] not in (state[2][0] for state in queue.heap)):

                    #    Like previous algorithms: we should check in this point if successor
                    #    is a goal state so as to follow lectures code

                    newPath = path + [item[1]]
                    pri = problem.getCostOfActions(newPath)

                    queue.push((item[0], newPath), pri)

                # State is in queue. Check if current path is cheaper from the previous one #
                elif item[0] not in visited and (item[0] in (state[2][0] for state in queue.heap)):
                    for state in queue.heap:
                        if state[2][0] == item[0]:
                            oldPri = problem.getCostOfActions(state[2][1])

                    newPri = problem.getCostOfActions(path + [item[1]])

                    # State is cheaper with his hew father -> update and fix parent #
                    if oldPri > newPri:
                        newPath = path + [item[1]]
                        queue.update((item[0], newPath), newPri)


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
class MyPriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, problem, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer
        self.problem = problem
    def push(self, item, heuristic):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(self.problem,item,heuristic))

def f(problem,state,heuristic):

    return problem.getCostOfActions(state[1]) + heuristic(state[0],problem)


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #  util.raiseNotDefined()


    queue = MyPriorityQueueWithFunction(problem,f)

    path = []
    visited = []

    # Check for gaol state at th initial state
    if problem.isGoalState(problem.getStartState()):
        return []
    node = (problem.getStartState(), [])
    queue.push(node, heuristic)

    while (True):
        # Terminate when nothing found
        if queue.isEmpty():
            return []
        # current state data
        xy, path = queue.pop()  # Take position and path

        '''State is already been visited. A path with lower cost has previously
             been found. Simply pass'''
        if xy in visited:
            continue
        visited.append(xy)
        # Terminate when goal is found
        if problem.isGoalState(xy):
            return path
            # find the successors of current state
        nextt = problem.getSuccessors(xy)
        # Add new states in queue and fix their path #
        if nextt:
            for item in nextt:
                if item[0] not in visited:
                    # Like previous algorithms: we should check in this point if successor
                    # is a goal state so as to follow lectures code

                    newPath = path + [item[1]]  # Fix new path
                    node = (item[0], newPath)
                    queue.push(node, heuristic)

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
