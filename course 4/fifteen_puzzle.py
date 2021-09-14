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
COL0_SOLUTION = 'ruldrdlurdluurddlur'
TOPRIGHT_SOLUTION = 'urdlurrdluldrruld'
TOPLEFT_SOLUTION = 'drul'

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

        row_i, col_j = num // self._grid_width, num % self._grid_width
        return row_i, col_j

    def clone(self):
        """returns a clone of myself"""
        height, width = self._grid_height, self._grid_width
        new_grid = Grid(height, width)
        for row_i in range(height):
            for col_j in range(width):
                if self.is_empty(row_i, col_j):
                    new_grid.set_empty(row_i, col_j)
                else:
                    new_grid.set_full(row_i, col_j)
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
        return self._value == other.get_value()

    def __ne__(self, other):
        """The value does not match equals no match"""
        return self._value != other.get_value()
    
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

    if start == target:  # no need to search
        return graph, node
    
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

def trace_root(node):
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
        return [node]

    trace = [node]  # starting one
    rest_trace = trace_root(parent_node)
    trace = rest_trace + trace  # just reversed the list start to end
    return trace

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
    start_pos = path[0].get_value()
    move_string = ''
    for node in path[1:]:  # get the start to target path
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

    # core helpers
    def _find_path(self, grid, start, target):
        """
        Finds the optimial path from start tile to target tile
        """
        _, target_node = create_path_graph(grid, start, target)
        if target_node is None:  # if no path to the target
            return None, None

        target_path = trace_root(target_node)
        target_path_str = path2moves(target_path)
        return target_path, target_path_str

    def _move_zero(self, path_grid, target_pos):
        """
        move tile 0 to the target position

        parameter
        ---------
        path_grid: Grid object that details the moveable area and obstacles
        target_pos: (row_i, col_j) of the desired position of the tile 0

        return 
        ------
        applied movement string for the tile 0, str
        """
        zero_pos = self.current_position(0, 0)
        shift_path, shift_path_str = self._find_path(path_grid, zero_pos, target_pos)
        assert shift_path is not None
        self.update_puzzle(shift_path_str)
        return shift_path_str

    def _move_target(self, path_grid, current_pos, desired_pos):
        """
        Use the tile 0 to move an internal tile to its target position

        parameter
        ---------
        path_grid: Grid object that details the moveable area and obstacles
        current_pos: (row_i, col_j) of the current target tile
        desired_pos: (row_i, col_j) of the desired position of the target tile

        return
        ------
        applied movement string for the tile 0, str
        """
        # path finding grid
        grid = path_grid
        
        # get moving path for the target tile
        # that will be used for tile 0 to move it
        cur_pos = current_pos
        num_anchor = self.get_number(cur_pos[0], cur_pos[1])
        target_pos = num_anchor//self._width, num_anchor%self._width

        target_path, target_path_str = self._find_path(grid.clone(), cur_pos, desired_pos)
        assert target_path is not None
        
        # getting where to move tile 0 to & update
        res = ''
        cur_pos = self.current_position(*target_pos)
        for idx, path_node in enumerate(target_path[1:]):
            shift_path_str = ''

            # need to move tile 0 to swap postiion
            # target tile is not movable while shifting tile 0
            shift_target = path_node.get_value()
            cur_pos = self.current_position(*target_pos)
            tmp_grid = grid.clone()
            tmp_grid.set_full(cur_pos[0], cur_pos[1])
            shift_path_str += self._move_zero(tmp_grid, shift_target)
            
            
            # actually swapping position with the target node
            swap_ms = DIRFLIP_MAP[target_path_str[idx]]
            self.update_puzzle(swap_ms)
            shift_path_str += swap_ms

            # update
            res += shift_path_str

        return res

    def _invariant_grid(self, target_row, target_col):
        """
        Create an OnOff Grid for path finding purpose
        that satistifies the 'lower_row_invariant' restriction
        """
        height, width = self._height, self._width
        # path finding grid
        grid = Grid(height, width)
        invariant_num = target_row * width + target_col
        total_cells = height * width
        
        # setting up obstacles
        if target_row >= 2:
            lower_invariant_num = invariant_num
        else:
            lower_invariant_num = 2 * (width - 1) + 1

        for num in range(lower_invariant_num + 1, total_cells):
            row_i, col_j = grid.get_index(num)
            grid.set_full(row_i, col_j)
        
        if target_row <= 1:
            inum_lst = []
            # for first two row invariant
            for idx in range(target_col, width-1):
                inum_lst.append(0 * width + idx + 1)
                inum_lst.append(1 * width + idx + 1)
            
            # for row0 invariant, below tile also unmutable
            if target_row == 0:
                inum_lst.append(1 * width + target_col)
            
            for inum in inum_lst:
                row_i, col_j = grid.get_index(inum)
                grid.set_full(row_i, col_j)
        
        return grid

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
        For a puzzle of m x z size, this method is for 
            all tiles in [2, m) rows
        
        parameter
        ---------
        target_row, target_col: row_i, col_j that specifizes the target tile

        return
        ------
        a stream of movement string for tile 0

        condition
        ---------
        lower_row_invariant is always true before and after
        """
        res = ''
        target_pos = target_row, target_col

        # path finding grid
        grid = self._invariant_grid(*target_pos)
        cur_pos = self.current_position(*target_pos)
        res += self._move_target(grid, cur_pos, target_pos)
        
        # realign tile 0 ready for the next solve
        tmp_grid = grid.clone()
        tmp_grid.set_full(*target_pos)
        res += self._move_zero(tmp_grid, (target_row, target_col - 1))
        return res

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (>= 2)
        Updates puzzle and returns a move string

        parameter
        ---------
        target_row: column is fixed, target row index

        return
        ------
        movement string, str

        condition
        ---------
        lower_row_invariant is True
        """
        res = ''
        target_col = 0
        zero_pos = self.current_position(0, 0)
        cur_pos = self.current_position(target_row, target_col)
        target_pos = target_row, target_col
        setup_pos = target_row - 1, 1  # setup position to use preset solution

        # path finding grid
        grid = self._invariant_grid(*target_pos)

        # sometime, the target tile could be right on top of the tile 0
        # moving 0 out solves it, but creates an awkard stuck case
        if cur_pos == (zero_pos[0]-1, zero_pos[1]):
            res += self._move_zero(grid.clone(), cur_pos)
        else:
            # moved target tile to the setup/solvable position
            res += self._move_target(grid.clone(), cur_pos, setup_pos)

            # moved tile 0 to the solvable position
            tmp_grid = grid.clone()
            tmp_grid.set_full(*setup_pos)
            res += self._move_zero(tmp_grid, (target_pos[0]-1, target_pos[1]))

            self.update_puzzle(COL0_SOLUTION)
            res += COL0_SOLUTION
        
        # realign tile 0 for next solve
        tmp_grid = grid.clone()
        tmp_grid.set_full(*target_pos)
        res += self._move_zero(tmp_grid, (target_pos[0]-1, self._width-1))
        return res

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)

        condition
        ---------
        - Tile 0 is at (0, target_col) position
        - all tiles at row_i > 1 are solved
        - all tiles between 0 >= row_i >= 1 and j > target_col are solved
        - tile below Tile 0 is solved (1, target_col)

        return
        ------
        True = yes, False = no
        """
        height, width = self.get_height(), self.get_width()
        
        if self.current_position(0,0) != (0, target_col):
            return False
        
        for row_i in range(2, height):
            for col_j in range(width):
                if self.current_position(row_i, col_j) != (row_i, col_j):
                    return False
        
        for col_j in range(target_col+1, width):
            for row_i in range(2):
                if self.current_position(row_i, col_j) != (row_i, col_j):
                    return False

        if self.current_position(1, target_col) != (1, target_col):
            return False

        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)

        condition
        ---------
        - Tile 0 is at (1, target_col) position
        - all tiles at row_i > 1 are solved
        - all tiles between 0 >= row_i >= 1 and j > target_col are solved

        return
        ------
        True = yes, False = no
        """
        height, width = self.get_height(), self.get_width()
        
        if self.current_position(0,0) != (1, target_col):
            return False
        
        for row_i in range(2, height):
            for col_j in range(width):
                if self.current_position(row_i, col_j) != (row_i, col_j):
                    return False

        for col_j in range(target_col+1, width):
            for row_i in range(2):
                if self.current_position(row_i, col_j) != (row_i, col_j):
                    return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        res = ''
        grid = self._invariant_grid(0, target_col)
        cur_pos, target_pos = self.current_position(0, target_col), (0, target_col)
        setup_pos = target_pos[0]+1, target_pos[1]-1
        zero_pos = self.current_position(0, 0)

        # sometime, the target tile could be right on left of the tile 0
        # moving 0 out solves it, but creates an awkard stuck case
        if cur_pos == (zero_pos[0], zero_pos[1]-1):
            res += self._move_zero(grid.clone(), cur_pos)

            # realign tile 0
            tmp_grid = grid.clone()
            tmp_grid.set_full(*target_pos)
            res += self._move_zero(tmp_grid, (setup_pos))
        else:
            # move target tile to desired setup position
            res += self._move_target(grid.clone(), cur_pos, setup_pos)

            # move tile 0 to setup position
            zero_setup_pos = setup_pos[0], setup_pos[1]-1  # to the right of target setup
            tmp_grid = grid.clone()
            tmp_grid.set_full(*setup_pos)
            res += self._move_zero(tmp_grid, zero_setup_pos)

            # use resolved setup solution
            # realign tile 0 no need, above did it
            self.update_puzzle(TOPRIGHT_SOLUTION)
            res += TOPRIGHT_SOLUTION
        
        return res

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        res = ''

        # move target tile to desired position
        cur_pos, target_pos = self.current_position(1, target_col), (1, target_col)
        grid = self._invariant_grid(1, target_col)
        res += self._move_target(grid.clone(), cur_pos, target_pos)


        # realign tile 0
        tmp_grid = grid.clone()
        tmp_grid.set_full(*target_pos)  # setup grid before mutate assignment
        target_pos = target_pos[0] -1, target_col
        res += self._move_zero(tmp_grid, target_pos)

        return res

    ###########################################################
    # Phase 3 methods

    def _is_solved(self):
        """Boolean Flag indicating whether the puzzle is solved or not"""
        height, width = self.get_height(), self.get_width()
        for row_i in range(height):
            for col_j in range(width):
                if self.current_position(row_i, col_j) != (row_i, col_j):
                    return False
        return True

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        The final 4s
        """
        res = ''
        grid = self._invariant_grid(1,1)
        res += self._move_zero(grid.clone(), (0, 0))  # moves to the origin

        # just keep making circle until its solved
        cnt = 0
        while not self._is_solved():
            if cnt > 3:
                # no solution
                break

            self.update_puzzle(TOPLEFT_SOLUTION)
            res += TOPLEFT_SOLUTION
            cnt += 1

        return res

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        res = ''
        height, width = self.get_height(), self.get_width()

        # start from the lower right
        mstr = self._move_zero(Grid(height, width), (height-1, width-1))
        res += mstr
        assert self.lower_row_invariant(height-1, width-1)

        # not include row 0 & 1, up to all other that are i > 1
        for row_i in range(height-1, 1, -1):
            for col_j in range(width-1, 0, -1):
                mstr = self.solve_interior_tile(row_i, col_j)
                res += mstr
                assert self.lower_row_invariant(row_i, col_j-1)

            mstr = self.solve_col0_tile(row_i)
            res += mstr
            assert self.lower_row_invariant(row_i-1, width-1)
        
        for col_j in range(width-1, 1, -1):
            assert self.row1_invariant(col_j)
            for row_i in range(1, -1, -1):
                if row_i == 1:
                    mstr = self.solve_row1_tile(col_j)
                    res += mstr
                else:
                    assert self.row0_invariant(col_j)
                    mstr = self.solve_row0_tile(col_j)
                    res += mstr
            assert self.row1_invariant(col_j - 1)
        
        mstr = self.solve_2x2()
        res += mstr

        return res


# %%
# Start interactive simulation
# import poc_fifteen_gui
# poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

