"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""
# %%
# helpers & algos
COORD2DIR_MAP = {
    (-1, 0): 'u',
    (1, 0): 'd',
    (0, -1): 'l',
    (0, 1): 'r',
}
DIRFLIP_MAP = {
    'u': 'd',
    'd': 'u',
    'l': 'r',
    'r': 'l'
}
EMPTY = 0
FULL = 1

class Grid:
    """
    Implementation of 2D grid of cells
    Includes boundary handling
    """
    
    def __init__(self, grid_height, grid_width):
        """
        Initializes grid to be empty, take height and width of grid as parameters
        Indexed by rows (left to right), then by columns (top to bottom)
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
                
    def __str__(self):
        """
        Return multi-line string represenation for grid
        """
        ans = ""
        for row in range(self._grid_height):
            ans += str(self._cells[row])
            ans += "\n"
        return ans
    
    def get_grid_height(self):
        """
        Return the height of the grid for use in the GUI
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Return the width of the grid for use in the GUI
        """
        return self._grid_width


    def clear(self):
        """
        Clears grid to be empty
        """
        self._cells = [[EMPTY for dummy_col in range(self._grid_width)]
                       for dummy_row in range(self._grid_height)]
                
    def set_empty(self, row, col):
        """
        Set cell with index (row, col) to be empty
        """
        self._cells[row][col] = EMPTY
    
    def set_full(self, row, col):
        """
        Set cell with index (row, col) to be full
        """
        self._cells[row][col] = FULL
    
    def is_empty(self, row, col):
        """
        Checks whether cell with index (row, col) is empty
        """
        return self._cells[row][col] == EMPTY
 
    def four_neighbors(self, row, col):
        """
        get horiz/vert neighbors of cell
        
        parameter
        ---------
        row: center tile row index i
        col: center tile column index j

        return
        ------
        [top, botton, left, right], None for nonexisting neighbor for placeholder
        """
        ans = []
        if row > 0:
            ans.append((row - 1, col))
        else:
            ans.append(None)
        
        if row < self._grid_height - 1:
            ans.append((row + 1, col))
        else:
            ans.append(None)
        
        if col > 0:
            ans.append((row, col - 1))
        else:
            ans.append(None)

        if col < self._grid_width - 1:
            ans.append((row, col + 1))
        else:
            ans.append(None)
        return ans
    
    def get_index(self, num):
        """return (row, col) given the number of tile based on left to right order"""
        if num >= self._grid_width * self._grid_height:
            raise ValueError('Number is too high')

        row_i, col_j = num // self._grid_height, num % self._grid_width
        return row_i, col_j

    def clone(self):
        height, width = self._grid_height, self._grid_width
        new_grid = Grid(height, width)
        for row_i in range(height):
            for col_j in range(width):
                new_grid._cells[row_i][col_j] = self._cells[row_i][col_j]
        return new_grid


class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return the number of items in the queue.
        """
        return len(self._items)
    
    def __iter__(self):
        """
        Create an iterator for the queue.
        """
        for item in self._items:
            yield item

    def __str__(self):
        """
        Return a string representation of the queue.
        """
        return str(self._items)

    def enqueue(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)

    def dequeue(self):
        """
        Remove and return the least recently inserted item.
        """
        return self._items.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []
        

class Node:
    """
    An simple node implementation that holds arbitary value
    with single parent and child undirected linking
    """

    def __init__(self, value):
        """
        initialize the object

        parameter
        ---------
        value: anythings that can be hashed
        """
        self._value = value
        self._parent = None
        self._child = None
    
    def __str__(self):
        """String representation"""
        return 'Node<{}>'.format(self._value)
    
    def __repr__(self):
        """The actual representation"""
        return self.__str__()
    
    def __eq__(self, other):
        """The value matches equals matches"""
        return self._value == other._value

    def __ne__(self, other):
        """The value does not match equals no match"""
        return self._value != other._value
    
    def __hash__(self):
        """Hashing the value field"""
        return hash(self._value)
    
    def get_value(self):
        """Get value field"""
        return self._value
    
    def get_parent(self):
        """Get parent node"""
        return self._parent

    def get_child(self):
        """Get child node"""
        return self._child

    def set_parent(self, parent):
        """Set new parent node"""
        self._parent = parent
    
    def remove_parent(self):
        """Remove the existing parent node"""
        self._parent = None
    
    def set_child(self, child):
        """Set new child node"""
        self._child = child
    
    def remove_child(self):
        """Remove the existing child node"""
        self._child = None


class SimpleGraph:
    """
    Simple graph implementation that utilize Node class
        holds onlt unique value of nodes
    """

    def __init__(self):
        """initialize the graph"""
        self._nodes = set()
    
    def __iter__(self):
        """provides iteration functionality"""
        for node in self._nodes:
            yield node
        
    def __len__(self):
        """be able to use len(...) on graph"""
        return len(self._nodes)
    
    def __contains__(self, other):
        """be able to use 'in' on graph"""
        return other in self._nodes
        
    def add_node(self, value):
        """add a node with given value"""
        node = Node(value=value)
        self._nodes.add(node)
        return node
    
    def find_node(self, value):
        """return the node object with the given value"""
        target_node = Node(value=value)
        for node in self:
            if node == target_node:
                return node
    
    def remove_node(self, value):
        """remove the node that has the given value"""
        node = self.find_node(value)
        self._nodes.remove(node)
        return node


def create_path_graph(grid, start, target):
    """
    Construct a path graph instance on a 2D grid space
        using breath-frist search approach to the find the shortest path
        between two given points

    parameter
    ---------
    grid: 2d grid object
    start: starting position of the path (row, col)
    target: ending position of the path (row, col)

    return
    ------
    (full graph, target_node): SimpleGraph object, Node object
        target_node could be None if there is no path available to the given target
    """
    que = Queue()
    graph = SimpleGraph()
    node = graph.add_node(start)
    que.enqueue(node)
    grid.set_full(start[0], start[1])

    # BFS search with early termination
    # when it first meets the target
    while len(que) > 0:
        parent_node = que.dequeue()
        pos = parent_node.get_value()

        for neigh in grid.four_neighbors(pos[0], pos[1]):
            # blocked, ignore or go around, nor no neighbor in that direction
            if neigh is None or not grid.is_empty(neigh[0], neigh[1]):
                continue 
            
            # create graph node
            node = graph.add_node(neigh)
            node.set_parent(parent_node)

            # add in queue
            que.enqueue(node)

            # set visited
            grid.set_full(neigh[0], neigh[1])

            # early termination
            if neigh == target:
                return graph, node
    
    return graph, None  # have not found the target


def trace_root(node, trace=[]):
    """
    Trace upward of a node all the way to the root node
        and create a path alone the way

    parameter
    ---------
    node: Node object

    return
    ------
    [start_node, step 1, step 2, ..., target_node]: order perserveres
    """
    parent_node = node.get_parent()
    if parent_node is None:
        # this is the root
        trace.append(node)
        return list(reversed(trace))
    
    trace.append(node)
    return trace_root(parent_node, trace)


def path2moves(path):
    """
    Create a list of moving string for the given path

    parameter
    ---------
    path: [start_node, node1, node2, ..., target_node]

    return
    ------
    sequential moving string according the path
    """
    start_pos = path.pop(0).get_value()
    move_string = ''
    for node in path:  # get the start to target path
        # caluclate incremental shift with its moving string
        target_pos = node.get_value()
        diff = (target_pos[0]-start_pos[0], target_pos[1]-start_pos[1])
        move_string += COORD2DIR_MAP[diff]
        start_pos = target_pos
    return move_string


# Main fifteen puzzle game class
class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved

        return
        ------
        (row_i, col_j): current position in the puzzle

        example
        -------
        current puzzle -> [[2,3],[0,1]]
        current_position(0,0) -> should be 0 is at the position of (1,0)
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the lower-right row invariant
        
        parameter
        ---------
        target_row, target_col: target tile position

        return
        ------
        boolean: True = passed, False = failed
        """
        height, width = self.get_height(), self.get_width()
        
        # check the zero tile is position correctly
        if self.current_position(0, 0) != (target_row, target_col):
            return False

        # all (row_i + 1) rows have to be solved
        for row_i in range(target_row+1, height):
            for col_j in range(width):
                if self.current_position(row_i, col_j) != (row_i, col_j):
                    return False
        
        # all same row_i, [col_j+1, width) have to be solved
        for col_j in range(target_col+1, width):
            if self.current_position(target_row, col_j) != (target_row, col_j):
                return False

        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        return ""

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        return ""


# %%
# Start interactive simulation
# import poc_fifteen_gui
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


# %%
# Some on fly tests

grid = Grid(4, 4)

# setting up obstacles
cur_pos, target_pos = (1, 2), (2, 2)
zero, zero_target = (2, 0), (0, 2)
invariant = 12
for num in range(invariant, 16):
    row_i, col_j = grid.get_index(num)
    grid.set_full(row_i, col_j)
grid.set_full(cur_pos[0], cur_pos[1])
print grid

graph, target_node = create_path_graph(grid.clone(), zero, zero_target)
path = trace_root(target_node, trace=[]) # path from target to start
print path
move_string = path2moves(path)
print move_string

graph, target_node = create_path_graph(grid.clone(), cur_pos, target_pos)
path = trace_root(target_node, trace=[]) # path from target to start
print path
move_string = path2moves(path)
print move_string
