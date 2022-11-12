def build_grid(r, c):
    grid = {}
    grid["(0,0)"]={"(0,1)":1, "(1,0)":1}
    grid["(0,%d)"%(c-1)]={"(1,%d)"%(c-1):1, "(0,%d)"%(c-2):1}
    grid["(%d,0)"%(r-1)]={"(%d,0)"%(r-2):1, "(%d,1)"%(r-1):1}
    grid["(%d,%d)"%((r-1),(c-1))]={
        "(%d,%d)"%((r-2),(c-1)):1, 
        "(%d,%d)"%((r-1),(c-2)):1}

    for i in range(c-2):
        grid["(0,%d)"%(i+1)]={
            "(0,%d)"%(i+2):1, 
            "(1,%d)"%(i+1):1, 
            "(0,%d)"%i:1}
        grid["(%d,%d)"%((r-1),(i+1))]={
            "(%d,%d)"%((r-2),(i+1)):1, 
            "(%d,%d)"%((r-1),(i+2)):1, 
            "(%d,%d)"%((r-1),i):1}

    for i in range(r-2):
        grid["(%d,0)"%(i+1)]={
            "(%d,0)"%i:1, 
            "(%d,1)"%(i+1):1, 
            "(%d,0)"%(i+2):1}
        grid["(%d,%d)"%((i+1),(c-1))]={
            "(%d,%d)"%(i,(c-1)):1, 
            "(%d,%d)"%((i+2),(c-1)):1, 
            "(%d,%d)"%((i+1),(c-2)):1}

    for i in range(r-2):
        for j in range(c-2):
            grid["(%d,%d)"%((i+1),(j+1))]={
                "(%d,%d)"%((i),(j+1)):1, 
                "(%d,%d)"%((i+1),(j+2)):1,
                "(%d,%d)"%((i+2),(j+1)):1, 
                "(%d,%d)"%((i+1),(j)):1
            }
    return grid

def build_locations(r, c):
    locations = {}
    for i in range(r):
        for j in range(c):
            locations["(%d,%d)"%(i,j)]=(i,j)
    return locations


class ChessBoard:
    #tenere a mente che per aggiungere gli ostacoli basta modificare questa classe
    def __init__(self, size, x_blocks, y_blocks, obstacles:list=[]):
        self.size = size
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks
        x_pixel = size-(size%x_blocks)
        self.bounds = (x_pixel, x_pixel*y_blocks/x_blocks)
        self.block_size = x_pixel/x_blocks

        self.grid = build_grid(self.x_blocks, self.y_blocks)
        self.locations = build_locations(self.x_blocks, self.y_blocks)