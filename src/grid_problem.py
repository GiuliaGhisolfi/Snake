from src.aima_search import Problem, PriorityQueue, Node, manhattan_distance, heapq, memoize, astar_search
import numpy as np

class GridProblem(Problem):
    """This class represents the problem of finding a path on a 2D grid."""
    
    def __init__(self, initial, goal, grid, hor_orient):
        super().__init__(initial, goal)
        self.grid = grid
        self.hor_orient = hor_orient
    
    def actions(self, state):
        """The available actions are the neighboring cells of the current one."""
        return self.grid[state]

    def result(self, state, action):
        """The result of an action is the action itself."""
        return action
    
    def h(self, state):
        """The heuristic used is Manhattan distance."""
        if isinstance(self.goal, list):
            min = np.inf
            for goal in self.goal:
                d = manhattan_distance(state.state, goal)
                if d < min:
                    min = d
            d = min
        else:
            d = manhattan_distance(state.state, self.goal)
        return d

class PriorityQueueTies(PriorityQueue):
    """A Queue in which the minimum (or maximum) element (as determined by f and
    forder) is returned first. If more than one element has the minimum 
    (or maximum) value of f, the element with the minimum (or maximum) value of 
    t (as determined by t and torder) is returned first.
    If forder is 'min', the item with minimum f(x) is returned first; 
    if forder is 'max', then it is the item with maximum f(x).
    If torder is 'min', when multiple elements have the minimum (or maximum) 
    value of f, the item with minimum t(x) is returned first; if torder is 
    'max', then it is the item with maximum t(x).
    Also supports dict-like lookup."""
    def __init__(self, forder='min', f=lambda x: x, torder='min', t=lambda x: x):
        super().__init__(forder, f)
        if torder == 'min':
            self.t = t
        elif torder == 'max':           # now item with max t(x)
            self.t = lambda x: -t(x)    # will be popped first in case of ties
        else:
            raise ValueError("Order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, [self.f(item), self.t(item), item])

    def pop(self):
        """Pop and return the item (with min or max f(x) value, breaking ties 
        with t(x) values) depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[2]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __contains__(self, key):
        """Return True if the key is in PriorityQueue."""
        return any([item == key for _, _, item in self.heap])

    def __getitem__(self, key):
        """Returns the first value associated with key in PriorityQueue.
        Raises KeyError if key is not present."""
        for value, _, item in self.heap:
            if item == key:
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key):
        """Delete the first occurrence of key."""
        try:
            del self.heap[[item == key for _, _, item in self.heap].index(True)]
        except ValueError:
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)

class GridNode(Node):
    """A grid node in a search tree. It has horizontal or vertical horientation
    (hor_orient is True or False respectively) depending on the orientation
    the agent has when it visits it. The attribute turn is True if the agent
    turned itself to reach this node (False oterwise)."""
    def __init__(
        self, 
        state, 
        hor_orient, 
        turn, 
        n_neighbors, 
        parent=None, 
        action=None, 
        path_cost=0):
        """Create a search tree GridNode, derived from a parent by an action."""
        super().__init__(state, parent, action, path_cost)
        self.hor_orient = hor_orient
        self.turn = turn
        self.n_neighbors = n_neighbors

    def child_node(self, problem, action):
        """Returns the tree GridNode generated by 'action'."""
        next_state = problem.result(self.state, action)
        turn = False
        new_hor_orient = self.hor_orient
        if self.hor_orient:
            if next_state[1] != self.state[1]:
                turn = True
                new_hor_orient = False
        else:
            if next_state[0] != self.state[0]:
                turn = True
                new_hor_orient = True
        next_node = GridNode(
            state=next_state, 
            hor_orient=new_hor_orient, 
            turn=turn, 
            n_neighbors=len(problem.actions(next_state)),
            parent=self, 
            action=action, 
            path_cost=problem.path_cost(
                self.path_cost, 
                self.state, 
                action, 
                next_state)
        )
        return next_node


def best_first_grid_search(problem, f, t, display=False):
    """Search the nodes of the grid with the lowest f scores first, breaking ties 
    with t scores (in case of a tie the nodes with minimum t score are seached 
    first).
    You specify the function f(node) that you want to minimize and t(node) that 
    you want to use to break ties; for example, if f is a heuristic estimate to 
    the goal, then we have greedy best first search; if f is node.depth then we 
    have breadth-first search.
    There is a subtlety: the lines "f = memoize(f, 'f')" and 
    "t = memoize(t, 't')" mean that the f and t values will be cached on the 
    nodes as they are computed. So after doing a best first search you can 
    examine the f and t values of the path returned."""
    if not isinstance(problem, GridProblem):
        raise ValueError("Problem must be a grid problem")
    f = memoize(f, 'f')
    t = memoize(t, 't')
    node = GridNode(
        state=problem.initial, 
        hor_orient=problem.hor_orient, 
        turn=False,
        n_neighbors=len(problem.actions(problem.initial))
    )
    frontier = PriorityQueueTies(forder='min', f=f, torder='min', t=t)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(
                    len(explored), "paths have been expanded and", 
                    len(frontier), "paths remain in the frontier"
                    )
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None

def astar_search_min_turns(problem, weights):
    """Weighted A* search with f(n) = w0*g(n) + w1*h(n) + w2*t(n), where g(n) is 
    the path cost to reach node n, h(n) is the heuristic defined in GridProblem, 
    t(n) is 1 if the snake turned itself to reach node n, 0 otherwise. 
    The function used to break ties is -g(n).
    This algorithm finds the opthimal path which minimizes the number of turns
    the snake needs to make.""" # TODO: t'ha senso?
    h = memoize(problem.h, 'h')
    return best_first_grid_search(
        problem, 
        lambda n: weights[0]*n.path_cost + weights[1]*h(n) + weights[2]*n.turn,
        lambda n: -(n.path_cost)
    )

def astar_search_saving_spaces(problem, weights):
    """Weighted A* search with f(n) = w0*g(n) + w1*h(n) + w2*neigh(n), where 
    g(n) is the path cost to reach node n, h(n) is the heuristic defined in 
    GridProblem, neigh(n) is the number of children of node n.
    The function used to break ties is -g(n).
    This algorithm may not find the optimal path since the actual heuristic 
    function it uses is not admissible. f(n) favors the expansion of nodes with 
    fewer children, which correspond to cells neighboring those occupied by the 
    snake and/or on the edge of the grid.
    """ # TODO: t ha senso?
    h = memoize(problem.h, 'h')
    return best_first_grid_search(
        problem, 
        lambda n: weights[0]*n.path_cost + weights[1]*h(n) + weights[3]*n.n_neighbors,
        lambda n: -(n.path_cost)
    )

def longest_path(grid, start, goal):
    """Computes an approximation of the longest path from start to goal on the 
    grid. Starting from the shortest path from start to goal it tries to extend
    (with 3 additional moves) pairs of path pieces."""
    def could_extend(path, curr, next, new1, new2):
        """Check if the path curr->new1-->new2-->next is valid (the edges must
        correspond to allowed moves on the grid and the path must not overlap 
        with the current path)."""
        return new1 in grid[path[curr]] and \
            new2 in grid[new1] and \
            path[next] in grid[new2] and \
            new1 not in path and \
            new2 not in path
    
    # Compute shortest path
    gp = GridProblem(start, goal, grid, False)
    node = astar_search(gp)
    path = []
    if node != None:
        path = node.solution()
        path.insert(0, start)
    else:
        return None
    
    # Extend shortest path
    curr = 0
    next = 1
    length = len(path)
    while next < length:
        curr_coord = path[curr]
        next_coord = path[next]
        if curr_coord[1] == next_coord[1]:
            # curr and next cells are one above/below the other =>
            # extends the path between the two moving first left and then 
            #   moving up or down depending on the position of next w.r.t curr
            # or moving first right and then 
            #   moving up or down depending on the position of next w.r.t curr
            orth1 = (curr_coord[0], curr_coord[1]-1)
            orth2 = (curr_coord[0], curr_coord[1]+1)
            if curr_coord[0] > next_coord[0]:
                adj1 = (curr_coord[0]-1, orth1[1])
                adj2 = (curr_coord[0]-1, orth2[1])
            else:
                adj1 = (curr_coord[0]+1, orth1[1])
                adj2 = (curr_coord[0]+1, orth2[1])
        else:
            # curr and next cells are one to the left/right of the other =>
            # extends the path between the two moving first up and then 
            #   moving right or left depending on the position of next w.r.t curr
            # or moving first down and then 
            #   moving right or left depending on the position of next w.r.t curr
            orth1 = (curr_coord[0]+1, curr_coord[1])
            orth2 = (curr_coord[0]-1,curr_coord[1])
            if curr_coord[1] < next_coord[1]:
                adj1 = (orth1[0], curr_coord[1]+1)
                adj2 = (orth2[0], curr_coord[1]+1)
            else:
                adj1 = (orth1[0], curr_coord[1]-1)
                adj2 = (orth2[0], curr_coord[1]-1)
        new1 = None
        new2 = None
        if could_extend(path, curr, next, orth1, adj1):
            new1 = orth1
            new2 = adj1
        elif could_extend(path, curr, next, orth2, adj2):
            new1 = orth2
            new2 = adj2
        if new1 and new2:
            path.insert(next, new1)
            path.insert(next+1, new2)
            length += 2
        else:
            curr += 1
            next += 1
    
    path.pop(0)
    return path
