from search import *

PESI = (1,0.1,0.1,0.1) #path_cost, h??????, turn, n_neighbours

class GridProblem(Problem):
    def __init__(self, initial, goal, grid, horizontal_orientation):
        super().__init__(initial, goal)
        self.grid = grid
        self.horizontal_orientation = horizontal_orientation
    
    def actions(self, state): 
        return self.grid[state]

    def result(self, state, action):
        return action
    
    def h(self, state): # Manhattan distance
        if isinstance(self.goal, list):
            min = np.inf
            for goal in self.goal:
                d = abs(state.state[0]-goal[0]) + abs(state.state[1]-goal[1])
                if d < min:
                    min = d
            d = min
        else:
            d = abs(state.state[0]-self.goal[0]) + abs(state.state[1]-self.goal[1])
        return d

# Gli elementi della coda vengono ordinati in base a f e in caso di pareggi in base a t
class PriorityQueueTies(PriorityQueue):

    def __init__(self, forder='min', f=lambda x: x, torder='min', t=lambda x: x):
        self.heap = []
        if forder == 'min':
            self.f = f
        elif forder == 'max':
            self.f = lambda x: -f(x)
        else:
            raise ValueError("Order must be either 'min' or 'max'.")
        
        if torder == 'min':
            self.t = t
        elif torder == 'max':
            self.t = lambda x: -t(x)
        else:
            raise ValueError("Order must be either 'min' or 'max'.")

    def append(self, item):
        """Insert item at its correct position."""
        heapq.heappush(self.heap, [self.f(item), self.t(item), item])

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
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

# Nodo "orientato", memorizza l'orientamento del serpente (orizzontale o verticale)
# e memorizza se quando è stato generato dal padre ha richiesto al serpente di svoltare
class GridNode(Node):

    def __init__(self, state, horizontal_orientation, turn, n_neighbours, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)
        self.horizontal_orientation = horizontal_orientation # True se il serpente lo visita muovendosi in orizzontale
        self.turn = turn # True se ha richiesto al serpente di svoltare per raggiungerlo
        self.n_neighbours = n_neighbours

    def child_node(self, problem, action):
        next_state = problem.result(self.state, action)
        turn = False
        new_horizontal_orientation = self.horizontal_orientation
        if self.horizontal_orientation:
            if next_state[1] != self.state[1]:
                turn = True
                new_horizontal_orientation = False
        else:
            if next_state[0] != self.state[0]:
                turn = True
                new_horizontal_orientation = True
        next_node = GridNode(
            state=next_state, 
            horizontal_orientation=new_horizontal_orientation, 
            turn=turn, 
            n_neighbours=len(problem.actions(next_state)),
            parent=self, 
            action=action, 
            path_cost=problem.path_cost(self.path_cost, self.state, action, next_state)
        )
        return next_node


def best_first_grid_search_dummy(problem, f, t, display=False):
    if not isinstance(problem, GridProblem):
        print("The problem must be a grid problem")
        exit()
    f = memoize(f, 'f')
    node = GridNode(
        state=problem.initial, 
        horizontal_orientation=problem.horizontal_orientation, 
        turn=False,
        n_neighbours=len(problem.actions(problem.initial))
    )
    frontier = PriorityQueueTies(forder='min', f=f, torder='min', t=t)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            if display:
                print(len(explored), "paths have been expanded and", len(frontier), "paths remain in the frontier")
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

def astar_search_opportunistic(problem, snake, grid_area):
    # prima approssimazione: la strategia cambia quando lo snake è lungo almeno un quarto dell'area della grid
    if(snake.length >= (grid_area / 4)):
        return astar_search_saving_spaces(problem)
    else:
        return astar_search_min_turns(problem)

def astar_search_min_turns(problem):
    h = memoize(problem.h, 'h')
    return best_first_grid_search_dummy(
        problem, 
        lambda n: PESI[0]*n.path_cost + PESI[1]*h(n) + PESI[2]*n.turn, # la f da minimizzare 
        lambda n: -(n.path_cost) # la funzione da minimizzare nel caso in cui ci siano più nodi con pari valore di f
    )

# individua il cammino che rimane più vicino al corpo
def astar_search_saving_spaces(problem):
    h = memoize(problem.h, 'h')
    return best_first_grid_search_dummy(
        problem, 
        lambda n: PESI[0]*n.path_cost + PESI[1]*h(n) + PESI[3]*n.n_neighbours, # la f da minimizzare 
        lambda n: -(n.path_cost) # la funzione da minimizzare nel caso in cui ci siano più nodi con pari valore di f
    )

# individua il cammino che rimane più vicino al corpo
def astar_search_inverse(problem):
    h = memoize(problem.h, 'h')
    return best_first_grid_search_dummy(
        problem, 
        lambda n: -n.path_cost,
        lambda n: n.turn # la funzione da minimizzare nel caso in cui ci siano più nodi con pari valore di f
    )

def longest_path(grid, start, goal):
    def could_extend(path, curr, next, new1, new2):
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
        return path
    
    # Extend shortest path
    curr = 0
    next = 1
    l = len(path)
    while next < l:
        curr_x = path[curr][0]
        curr_y = path[curr][1]
        if path[curr][1] == path[next][1]:
            orth1 = (curr_x, curr_y-1)
            orth2 = (curr_x, curr_y+1)
            if curr_x > path[next][0]:
                adj1 = (curr_x-1, orth1[1])
                adj2 = (curr_x-1, orth2[1])
            else:
                adj1 = (curr_x+1, orth1[1])
                adj2 = (curr_x+1, orth2[1])
        else:
            orth1 = (curr_x+1, curr_y)
            orth2 = (curr_x-1,curr_y)
            if curr_y < path[next][1]:
                adj1 = (orth1[0], curr_y+1)
                adj2 = (orth2[0], curr_y+1)
            else:
                adj1 = (orth1[0], curr_y-1)
                adj2 = (orth2[0], curr_y-1)
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
            l += 2
        else:
            curr += 1
            next += 1
    
    path.pop(0)
    return path
