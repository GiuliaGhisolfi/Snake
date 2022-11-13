from search import *

class GridProblem(GraphProblem):
    def h(self, node):
        locs = getattr(self.graph, 'locations', None)
        if locs:
            if type(node) is str:
                return manhattan_distance(locs[node], locs[self.goal])

            return manhattan_distance(locs[node.state], locs[self.goal])
        else:
            return np.inf