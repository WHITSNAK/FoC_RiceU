"""
Clone of 2048 game.
"""
# %%
import random

INIT_TILES = 2

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    result = []
    
    first = None
    for num in line:
        # ignore 0s
        if num == 0:
            continue
        
        # finding anchor
        if not first:
            first = num
            continue
        
        # only adds when they the same, and once
        if first == num:
            result.append(first + num)
            first = None
        else:
            result.append(first)
            first = num
    
    # maybe some leftover not appended
    if first:
        result.append(first)
    
    # append the ending 0s to match dimensions
    result += [0] * (len(line)-len(result))
    return result


def empty_tiles(grid):
    """
    Return a list of tuple indices that maps to tiles that are empty
    """
    lst = []
    for row_i, row in enumerate(grid):
        for col_j, col in enumerate(row):
            if col == 0:
                lst.append((row_i, col_j))
    return lst


class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        # replace with your code
        self._height = grid_height
        self._width = grid_width
        self._grid = None
        self.reset()
        
        self._dir_indices = {key: [] for key in OFFSETS.keys()}
        for key in OFFSETS.keys():
            if key == UP:
                self._dir_indices[key] = [(0,i) for i in range(self._width)]
            elif key == DOWN:
                self._dir_indices[key] = [(self._height-1,i) for i in range(self._width)]
            elif key == LEFT:
                self._dir_indices[key] = [(i,0) for i in range(self._height)]
            elif key == RIGHT:
                self._dir_indices[key] = [(i,self._width-1) for i in range(self._height)]
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0]*self._width for _ in range(self._height)]
        for _ in range(INIT_TILES):
            self.new_tile()
    
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        string = ''
        for row in self._grid:
            chunk = '[' + ', '.join([str(r) for r in row]) + ']\n'
            string += chunk
        return string
    
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width
    
    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        indices = self._dir_indices[direction]
        offset = OFFSETS[direction]
        had_change = False
        
        for first in indices:
            # for each initial index
            # generate its trace tile values and trace grid indices
            start_idx = list(first)
            idx_lst = [tuple(start_idx)]
            tile_lst = [self.get_tile(start_idx[0], start_idx[1])]
            while True:
                start_idx[0] += offset[0]
                start_idx[1] += offset[1]
                
                if not self.is_in_grid(start_idx[0], start_idx[1]):
                    break
                
                idx_lst.append(tuple(start_idx))
                tile_lst.append(self.get_tile(start_idx[0], start_idx[1]))
            
            # merge & update all
            merged_vs = merge(tile_lst)
            for vs_i, idx in enumerate(idx_lst):
                new_v = merged_vs[vs_i]
                if not had_change:  # change flag checking if needed
                    old_value = self.get_tile(idx[0], idx[1])
                    had_change = old_value != new_v
                self.set_tile(idx[0], idx[1], new_v)
        
        # generate a new tile if there are changes
        if had_change:
            self.new_tile()

    def is_in_grid(self, row, col):
        """
        Given an index, return True or False
        if the index belong to the Grid. No wrapping, no negatives
        """
        in_row = row >= 0 and row <= self._height-1
        in_col = col >= 0 and col <= self._width-1
        return in_row and in_col
    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        if random.random() > 0.1:
            num = 2
        else:
            num = 4
        
        empties = empty_tiles(self._grid)
        selected = random.choice(empties)
        self.set_tile(selected[0], selected[1], num)
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


# GUI
if __name__ == '__main__':
    import poc_2048_gui

    poc_2048_gui.run_gui(TwentyFortyEight(4, 4))


# %%
