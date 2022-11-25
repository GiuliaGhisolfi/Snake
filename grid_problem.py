from search import *

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


def best_first_grid_search_min_turns(problem, f, t, display=False):
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
    return best_first_grid_search_min_turns(
        problem, 
        lambda n: n.path_cost + h(n) + n.turn, # la f da minimizzare 
        lambda n: -(n.path_cost) # la funzione da minimizzare nel caso in cui ci siano più nodi con pari valore di f
    )

# individua il cammino che rimane più vicino al corpo
def astar_search_saving_spaces(problem):
    h = memoize(problem.h, 'h')
    return best_first_grid_search_min_turns(
        problem, 
        lambda n: n.path_cost + h(n) + n.n_neighbours, # la f da minimizzare 
        lambda n: -(n.path_cost) # la funzione da minimizzare nel caso in cui ci siano più nodi con pari valore di f
    )

