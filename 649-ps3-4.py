import timeit
from heapq import heappush, heappop

class GridTile:
    def __init__(self, posX, posY):
        self.x = posX
        self.y = posY

        self.left = None
        self.right = None
        self.up = None
        self.down = None

        self.isObstacle = False
    
    def __str__(self):
        return f"({self.x},{self.y})"

def h(n : GridTile, goalx: int, goaly: int):
    if n == None:
        return 500

    return abs(n.x - goalx) + abs(n.y - goaly)

class Grid:
    def __init__(self, dimX, dimY):
        self.dimX = dimX
        self.dimY = dimY

        self.grid = []
        for _ in range(self.dimY):
            self.grid.append([])
        
        for y in range(self.dimY):
            for x in range(self.dimX):
                self.grid[y].append(GridTile(x, y))
    
        for y in range(self.dimY):
            for x in range(self.dimX):
                self.grid[y][x].left = self.grid[y][x-1] if x-1 >= 0 else None
                self.grid[y][x].right = self.grid[y][x+1] if x+1 < dimX else None
                self.grid[y][x].up = self.grid[y-1][x] if y-1 >= 0 else None
                self.grid[y][x].down = self.grid[y+1][x] if y+1 < dimY else None
    
    def setObstacle(self, x, y):
        self.grid[y][x].isObstacle = True

    def forward_search(self, initx, inity, goalx, goaly, mode):
        start = timeit.default_timer()
        n : GridTile = self.grid[inity][initx]
        newreach = [n.left, n.up, n.right, n.down]

        reachable = dict()
        reachable[n] = 0
        for m in newreach:
            if m != None:
                reachable[m] = 1

        while len(newreach) > 0:
            b : GridTile = newreach.pop(0)
            if b == None:
                continue

            if b.x == goalx and b.y == goaly:
                print(f"Goal found! moves={reachable[b]}, elapsed={timeit.default_timer() - start}")
                break
            
            poss_moves = [b.left, b.up, b.right, b.down]
            
            if mode == "BFS":
                for move in poss_moves:
                    if move == None or move.isObstacle:
                        continue

                    if move not in reachable:
                        newreach.insert(poss_moves.index(move), move)
                        reachable[move] = reachable[b]+1

                    else:
                        if reachable[b]+1 < reachable[move]:
                            print("revised", b, move, reachable[b]+1, reachable[move])
                            reachable[move] = reachable[b] + 1
            else:
                if mode == "greedy":
                    poss_moves.sort(key=lambda x: h(x, goalx, goaly))
                elif mode == "astar":
                    poss_moves.sort(key=lambda x: h(x, goalx, goaly))

                for move in poss_moves:
                    if move == None or move.isObstacle:
                        continue

                    if move not in reachable:
                        reachable[move] = reachable[b]+1

                        gmove = reachable[move]
                        hmove = h(move, goalx, goaly)
                        if mode == "greedy":
                            newreach.insert(hmove, move)
                        elif mode == "astar":
                            newreach.insert(hmove+gmove, move)
                    
                    else:
                        if reachable[b] + 1 < reachable[move]:
                            print("revised", b, move, reachable[b]+1, reachable[move])
                            reachable[move] = reachable[b]+1

grid = Grid(8,4)
obstacles = [(2,1),(3,1),(4,1),(5,1),(5,2),(5,3)]
for obstacle in obstacles:
    grid.setObstacle(obstacle[0], obstacle[1])

grid.forward_search(2, 3, 6, 3, 'BFS')
grid.forward_search(2, 3, 6, 3, 'greedy')
grid.forward_search(2, 3, 6, 3, 'astar')