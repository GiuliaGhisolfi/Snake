from search import *
from grid_problem import *

def longest_path(grid, start, goal):
    def could_extend(path, curr, next, new1, new2):
        return new1 in grid[path[curr]] and \
            new2 in grid[new1] and \
            path[next] in grid[new2] and \
            new1 not in path and \
            new2 not in path
    
    # Compute shortest path
    gp = GridProblem(start, goal, grid)
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
