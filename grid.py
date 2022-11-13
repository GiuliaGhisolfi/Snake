class Grid:
    # TODO: modificare questa classe per aggiungere ostacoli
    def __init__(self, size, x_blocks, y_blocks):
        self.size = size
        self.x_blocks = x_blocks
        self.y_blocks = y_blocks
        x_pixel = size-(size % x_blocks)
        self.bounds = (x_pixel, x_pixel*y_blocks/x_blocks)
        self.block_size = x_pixel/x_blocks
        self.build_grid()

    def build_grid(self):
        self.grid = {} #immutabile
        self.grid["(0,0)"] = {"(0,1)": 1, "(1,0)": 1}
        self.grid["(0,%d)" % (self.y_blocks-1)] = {"(1,%d)" % (self.y_blocks-1): 1, "(0,%d)" % (self.y_blocks-2): 1}
        self.grid["(%d,0)" % (self.x_blocks-1)] = {"(%d,0)" % (self.x_blocks-2): 1, "(%d,1)" % (self.x_blocks-1): 1}
        self.grid["(%d,%d)" % ((self.x_blocks-1), (self.y_blocks-1))] = {
            "(%d,%d)" % ((self.x_blocks-2), (self.y_blocks-1)): 1,
            "(%d,%d)" % ((self.x_blocks-1), (self.y_blocks-2)): 1}

        for i in range(self.y_blocks-2):
            self.grid["(0,%d)" % (i+1)] = {
                "(0,%d)" % (i+2): 1,
                "(1,%d)" % (i+1): 1,
                "(0,%d)" % i: 1}
            self.grid["(%d,%d)" % ((self.x_blocks-1), (i+1))] = {
                "(%d,%d)" % ((self.x_blocks-2), (i+1)): 1,
                "(%d,%d)" % ((self.x_blocks-1), (i+2)): 1,
                "(%d,%d)" % ((self.x_blocks-1), i): 1}

        for i in range(self.x_blocks-2):
            self.grid["(%d,0)" % (i+1)] = {
                "(%d,0)" % i: 1,
                "(%d,1)" % (i+1): 1,
                "(%d,0)" % (i+2): 1}
            self.grid["(%d,%d)" % ((i+1), (self.y_blocks-1))] = {
                "(%d,%d)" % (i, (self.y_blocks-1)): 1,
                "(%d,%d)" % ((i+2), (self.y_blocks-1)): 1,
                "(%d,%d)" % ((i+1), (self.y_blocks-2)): 1}

        for i in range(self.x_blocks-2):
            for j in range(self.y_blocks-2):
                self.grid["(%d,%d)" % ((i+1), (j+1))] = {
                    "(%d,%d)" % ((i), (j+1)): 1,
                    "(%d,%d)" % ((i+1), (j+2)): 1,
                    "(%d,%d)" % ((i+2), (j+1)): 1,
                    "(%d,%d)" % ((i+1), (j)): 1
                }
        return self.grid
