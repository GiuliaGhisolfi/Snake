from search import *
import re


class A_star:
    def __init__(self, problem, goal_state):
        self.problem = problem
        self.goal_state = goal_state
    
    def start(self):
        return astar_search(self.problem, self.heuristic)

    def heuristic(self, node):
        #Manhattan distance
        head = re.findall('(\d+)', node.state) # trova gli interi all'interno della stringa che rappresenta lo stato
        goal = re.findall('(\d+)', self.goal_state)
        return abs(int(goal[0]) - int(head[0])) + abs(int(goal[1]) - int(head[1]))