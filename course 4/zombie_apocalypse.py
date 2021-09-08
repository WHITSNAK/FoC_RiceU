"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human
    on a grid with obstacles
    """

    def __init__(self, grid_height, grid_width,
                 obstacle_list=None, zombie_list=None, human_list=None):
        """
        Create a simulation of given size with given
        obstacles, humans, and zombies

        parameter
        ---------
        grid_height, grid_width: int, size for the grid
        obstacle_list, zombie_list, human_list: [(row_i, col_j) ...]
            list of postion tuples on the grid to initialize
            default -> empties
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)  # use the original to clear up the cells
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        compute the 2D manhattan distance field
        based on the given entity_type as the center(s) and 4-way direction
        It also takes in account of obstacles

        parameter
        ---------
        entity_type: ZOMBIE, HUMAN

        return
        ------
        2D Grid in [[...]...]
        """
        if entity_type == ZOMBIE:
            func = self.zombies
        elif entity_type == HUMAN:
            func = self.humans
        
        dist = grids_min(*[self._simple_distance_field(entity) for entity in func()])
        return dist
        
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_human_lst = []
        for human in self.humans():
            # human wants to maximize distance
            max_dist, pos_lst = float('-inf'), []
            current_dist = zombie_distance_field[human[0]][human[1]]
            for neigh in self.eight_neighbors(human[0], human[1]):
                if not self.is_empty(neigh[0], neigh[1]):
                    continue

                dist = zombie_distance_field[neigh[0]][neigh[1]]
                if current_dist > dist:
                    continue
                elif dist > max_dist:
                    max_dist, pos_lst = dist, [neigh]
                elif dist == max_dist:
                    pos_lst.append(neigh)
            
            if pos_lst:
                new_pos = random.choice(pos_lst)
            else:
                new_pos = human
            new_human_lst.append(new_pos)
        
        self._human_list = new_human_lst
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_zombie_lst = []
        for zombie in self.zombies():
            # zombine wants brain and wants to minimize distance
            min_dist, pos_lst = float('inf'), []
            current_dist = human_distance_field[zombie[0]][zombie[1]]
            
            # zombie can only walk 4 directions
            for neigh in self.four_neighbors(zombie[0], zombie[1]):
                if not self.is_empty(neigh[0], neigh[1]):
                    continue
                
                dist = human_distance_field[neigh[0]][neigh[1]]
                if current_dist < dist:
                    continue
                elif dist < min_dist:
                    min_dist, pos_lst = dist, [neigh]
                elif dist == min_dist:
                    pos_lst.append(neigh)
            
            if pos_lst:
                new_pos = random.choice(pos_lst)
            else:
                new_pos = zombie
            new_zombie_lst.append(new_pos)
        
        self._zombie_list = new_zombie_lst
    
    
    def _enqueue_all_neighbors(self, queue, pos, step):
        """
        Store all 4-way neighbors ceils into the queue
        based on the given center position
        
        Specific data structure for calculating the distance field
        format: ((row, col), source step)
        """
        neighs = [(tuple(nei), step) for nei in self.four_neighbors(pos[0], pos[1])]
        for neigh in neighs:
            queue.enqueue(neigh)
    
    def _simple_distance_field(self, center):
        """
        Calcualte the distance field based on only one center position value
        """
        width, height = self.get_grid_width(), self.get_grid_height()
        dist = create_grid(height, width, width * height)  # max value
        visited = create_grid(height, width, 0)  # 0 grid
        que = poc_queue.Queue()  # breadth first search queue

        # (position tuple, source step)
        self._enqueue_all_neighbors(que, center, 0)
        dist[center[0]][center[1]] = EMPTY
        visited[center[0]][center[1]] = FULL

        # visit all squares in a grid
        while len(que) != 0:
            center, step = que.dequeue()
            center_x, center_y = center

            # only visit once
            if visited[center_x][center_y] == 1:
                continue
            
            # checks obstacle if not empty 
            if not self.is_empty(center_x, center_y):
                visited[center_x][center_y] = 1
                continue

            dist[center_x][center_y] = step + 1
            visited[center_x][center_y] = 1
            self._enqueue_all_neighbors(que, center, step + 1)
        
        return dist


# helper functions
def grids_min(*grids):
    """
    Create a global minimized grid given a list of grids
        only the smallest value for each square is chosen

    parameter
    ---------
    *grids: list of 2D grids in same size

    return
    ------
    a new grid in the same size
    """
    height, width = len(grids[0]), len(grids[0][0])
    new_grid = create_grid(height, width, 0)

    for row_i in range(height):
        for col_j in range(width):
            min_v = min(grid[row_i][col_j] for grid in grids)
            new_grid[row_i][col_j] = min_v
    
    return new_grid


def create_grid(height, width, val=0):
    """
    Convenient helper to create 2D Grid with arbitary value filling
    """
    if height == 0 or width == 0:
        return []

    return [[val for _ in range(width)] for _ in range(height)]



# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# import poc_zombie_gui
# poc_zombie_gui.run_gui(Apocalypse(30, 40))
