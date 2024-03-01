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
    return [s, s, w, s, w, w, s, w]


class Node:
    def __init__(self, parent, state, action, cost):
        self.parent = parent
        self.state = state
        self.action = action
        self.cost = cost
    def __eq__(self, other):
        return self.state==other.state


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
"""
    # print("Start:", problem.getStartState())
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    # ns,a,_=(problem.getSuccessors(problem.getStartState()))[0]
    # ns2,a2,_=problem.getSuccessors(ns)[0]
    # return [a,a2]
    "*** YOUR CODE HERE ***"
    frontier=util.Stack()
    "frontier.push((problem.getStartState(),[]))"
    frontier.push(Node(None, problem.getStartState(), None, 0))
    expanded=[]
    while not frontier.isEmpty():
        currentNode=frontier.pop()
        path=[]
        if problem.isGoalState(currentNode.state):
            while currentNode.parent:
                path=path+[currentNode.action]
                currentNode=currentNode.parent
            path.reverse()
            return path
        expanded.append(currentNode.state)
        for ns,a,_ in problem.getSuccessors(currentNode.state):
            if ns not in expanded:
                frontier.push(Node(currentNode,ns,a,0))
    return[]

def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    "frontier.push((problem.getStartState(),[]))"
    frontier=util.Queue()
    frontier.push(Node(None, problem.getStartState(), None, 0))
    expanded=set()
    while not frontier.isEmpty():
        currentNode=frontier.pop()
        if problem.isGoalState(currentNode.state):
            path=[]
            while currentNode.parent:
                path=path+[currentNode.action]
                currentNode=currentNode.parent
            path.reverse()
            return path
        expanded.add(currentNode.state)
        for ns,a,_ in problem.getSuccessors(currentNode.state):
            if ns not in expanded:
                frontier.push(Node(currentNode,ns,a,0))
                expanded.add(ns)
    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    "frontier.push((problem.getStartState(),[]))"
    # ucs
    frontier=util.PriorityQueue()
    startS=problem.getStartState();
    frontier.push(Node(None,startS,None,0),0)
    closed_set={}
    while not frontier.isEmpty():
        currentNode=frontier.pop()
        if problem.isGoalState(currentNode.state):
            path=[]
            while currentNode.parent:
                path=path+[currentNode.action]
                currentNode=currentNode.parent
            path.reverse()
            return path
        new_cost=0
        if (currentNode.state not in closed_set) or (currentNode.cost<closed_set[currentNode.state]):
            closed_set[currentNode.state]=currentNode.cost
            for ns,a,cost in problem.getSuccessors(currentNode.state):
                if (ns not in closed_set) or (cost<closed_set[ns]):
                    new_cost=currentNode.cost+cost
                    frontier.push(Node(currentNode,ns,a,new_cost),new_cost)
    # util.raiseNotDefined()
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    "frontier.push((problem.getStartState(),[]))"
    # astar
    frontier=util.PriorityQueue()
    startS=problem.getStartState()
    startNode=Node(None,startS,None,0)
    frontier.push(startNode,0+heuristic(startS,problem))
    closed_set=set()
    while not frontier.isEmpty():
        currentNode=frontier.pop()
        if problem.isGoalState(currentNode.state):
            path=[]
            while currentNode.parent:
                path=path+[currentNode.action]
                currentNode=currentNode.parent
            path.reverse()
            return path
        if currentNode.state not in closed_set:
            closed_set.add(currentNode.state)
            for ns,a,cost in problem.getSuccessors(currentNode.state):
                # the sum of the costs of all actions taken to date
                new_cost=currentNode.cost+cost
                heuristic_cost=new_cost+heuristic(ns,problem)
                frontier.push(Node(currentNode,ns,a,new_cost),heuristic_cost)
    # util.raiseNotDefined()
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
