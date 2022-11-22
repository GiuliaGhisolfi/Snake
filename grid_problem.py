from search import *

""" 
REVIEW: 
Questa implementazione di a* individua il percorso ottimo minimizzando il numero di "svolte" del serpente
e, se necessario, facendo svoltare il serpente il più lontano possibile dal nodo di partenza.
E' PROVVISORIA, devo ancora verificarne la correttezza e scriverla in modo più pulito.
Se ci sono problemi per tornare all'implementazione precedente basta sostituire nel file bot_singleplayer.py
GridProblem(start, False, goal, graph) con GridProblem(start, goal, graph) e 
astar_search_min_turns(grid_problem) con astar_search(grid_problem).
"""

'''Magari modificare la chaiamta di inizializzazione GridProblem, spostando False alla fine dell'elenco degli
argomenti, che mi ammazza da vedere.'''

# L'euristica utilizza dai problemi istanze della classe GridProblem è la distanza di Manhattan
class GridProblem(GraphProblem):

    def __init__(self, initial, horizontal_orientation, goal, graph):
        super().__init__(initial, goal, graph)
        self.horizontal_orientation = horizontal_orientation
    
    def h(self, node):
        locs = getattr(self.graph, 'locations', None)
        if locs:
            if type(node) is str:
                return manhattan_distance(locs[node], locs[self.goal])
            
            return manhattan_distance(locs[node.state], locs[self.goal])
        else:
            return np.inf

# Gli elementi della coda vengono ordinati in base a f e in caso di pareggi in base a t
class PriorityQueueTies:

    def __init__(self, forder='min', f=lambda x: x, torder='min', t=lambda x: x):
        self.heap = []
        if forder == 'min':
            self.f = f
        elif forder == 'max':  # now item with max f(x)
            self.f = lambda x: -f(x)  # will be popped first
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

    def extend(self, items):
        """Insert each item in items at its correct position."""
        for item in items:
            self.append(item)

    def pop(self):
        """Pop and return the item (with min or max f(x) value)
        depending on the order."""
        if self.heap:
            return heapq.heappop(self.heap)[2]
        else:
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self):
        """Return current capacity of PriorityQueue."""
        return len(self.heap)

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
class OrientedNode(Node):

    def __init__(self, state, horizontal_orientation, turn=False, parent=None, action=None, path_cost=0):
        super().__init__(state, parent, action, path_cost)
        self.horizontal_orientation = horizontal_orientation # True se il serpente lo visita muovendosi in orizzontale
        self.turn = turn # True se ha richiesto al serpente di svoltare per raggiungerlo
    
    def set_neighbours(self, neighbours):
        self.neighbours = neighbours

    def child_node(self, problem, action):
        """[Figure 3.10]"""
        next_state = problem.result(self.state, action)
        locs = getattr(problem.graph, 'locations', None)
        curr_loc = locs[self.state]
        next_loc = locs[next_state]
        turn = False
        new_horizontal_orientation = self.horizontal_orientation
        if self.horizontal_orientation:
            if next_loc[1] != curr_loc[1]:
                turn = True
                new_horizontal_orientation = False
        else:
            if next_loc[0] != curr_loc[0]:
                turn = True
                new_horizontal_orientation = True
        next_node = OrientedNode(
            next_state, 
            new_horizontal_orientation, 
            turn, 
            self, 
            action, 
            problem.path_cost(self.path_cost, self.state, action, next_state)
        )
        return next_node


def best_first_graph_search_min_turns(problem, f, t, display=False):
    if not isinstance(problem, GridProblem): # Può essere effettuata solo su griglie
        print("The problem must be a grid problem")
        return None
    f = memoize(f, 'f')
    node = OrientedNode(problem.initial, problem.horizontal_orientation)
    node.set_neighbours(len(problem.actions(node.state)))
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
            child.set_neighbours(len(problem.actions(child.state)))
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
    return best_first_graph_search_min_turns(
        problem, 
        lambda n: n.path_cost + h(n) + n.turn + n.neighbours , # la f da minimizzare 
        lambda n: n.path_cost # la funzione da massimizzare nel caso in cui ci siano più nodi con pari valore di f
    )

# individua il cammino che rimane più vicino al corpo
def astar_search_saving_spaces(problem):
    h = memoize(problem.h, 'h')
    return best_first_graph_search_min_turns(
        problem, 
        lambda n: n.path_cost + h(n) + n.neighbours, # la f da minimizzare 
        lambda n: n.path_cost # la funzione da massimizzare nel caso in cui ci siano più nodi con pari valore di f
    )

