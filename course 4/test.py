["""
An example of creating a distance field using Manhattan distance
"""
# %%
GRID_HEIGHT = 6
GRID_WIDTH = 8


def manhattan_distance(row0, col0, row1, col1):
    """
    Compute the Manhattan distance between the cells
    (row0, col0) and (row1, col1)
    """
    return abs(row0-row1) + abs(col0-col1)
        

def create_distance_field(entity_list):
        """
        Create a Manhattan distance field that contains the minimum distance to 
        each entity (zombies or humans) in entity_list
        Each entity is represented as a grid position of the form (row, col) 
        """
        field = []
        for row_i in range(GRID_HEIGHT):
            row = []
            for col_j in range(GRID_WIDTH):
                min_dis = float('inf')
                for entity in entity_list:
                    min_dis = min(min_dis, manhattan_distance(row_i, col_j, entity[0], entity[1]))
                row.append(min_dis)
            
            field.append(row)
        return field
        
    
def print_field(field):
    """
    Print a distance field in a human readable manner with 
    one row per line
    """
    for row in field:
        print row

def run_example():
    """
    Create and print a small distance field
    """
    field = create_distance_field([[4, 0],[2, 5]])
    print_field(field)
    
run_example() 

# Sample output for the default example
#[4, 5, 5, 4, 3, 2, 3, 4]
#[3, 4, 4, 3, 2, 1, 2, 3]
#[2, 3, 3, 2, 1, 0, 1, 2]
#[1, 2, 3, 3, 2, 1, 2, 3]
#[0, 1, 2, 3, 3, 2, 3, 4]
#[1, 2, 3, 4, 4, 3, 4, 5]
    
    

# %%
from poc_queue import Queue


GRID_HEIGHT = 6
GRID_WIDTH = 8

def get_4neighbor(pos):
    row_i, col_j = pos[0], pos[1]
    _pos = tuple(pos)

    neighbors = [
        (max(0, row_i-1), col_j),
        (min(GRID_HEIGHT-1, row_i+1), col_j),
        (row_i, min(GRID_WIDTH-1, col_j+1)),
        (row_i, max(0, col_j-1)),
    ]

    return filter(lambda x: x!=_pos, neighbors)

def enqueue_all_neighbors(pos, queue, step, neighbor_func):
    neighs = [(nei, step) for nei in neighbor_func(pos)]
    for neigh in neighs:
        que.enqueue(neigh)


def create_distance_field(pos, neighbor_func):
    dist = [[GRID_WIDTH * GRID_HEIGHT for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    visited = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    queue_z = Queue()

    # (positive tuple, source step)
    enqueue_all_neighbors(pos, queue_z, 0, neighbor_func)
    dist[pos[0]][pos[1]] = 0
    visited[pos[0]][pos[1]] = 1

    while len(queue_z) != 0:
        block_p, step = queue_z.dequeue()
        x, y = block_p

        if visited[x][y] == 1:
            continue
        
        if (x,y) in obstacles:
            visited[x][y] = 1
            continue

        dist[x][y] = step + 1
        visited[x][y] = 1
        enqueue_all_neighbors(block_p, queue_z, step + 1, neighbor_func)
    
    return dist


def grids_min(*grids):
    height, width = len(grids[0]), len(grids[0][0])
    new_grid = [[0 for _ in range(width)] for _ in range(height)]

    for row_i in range(height):
        for col_j in range(width):
            min_v = min(grid[row_i][col_j] for grid in grids)
            new_grid[row_i][col_j] = min_v
    
    return new_grid


# zombie_ps = [(0,1), (5,5), (2,3)]
zombie_ps = [(0,1)]
obstacles = [(0,2), (4,4),(1,1)]
grid = grids_min(*[
    create_distance_field(pos, get_4neighbor)
    for pos in zombie_ps
])

for row in grid:
    print row
