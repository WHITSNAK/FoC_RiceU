# unittests
import poc_simpletest, random
from game_2048 import merge, empty_tiles, TwentyFortyEight
from utils import grid_sum, compare_grid


# test helper functions
def setup_grid(game, grid):
    game.reset()
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            game.set_tile(i, j, v)


# tests
def test_merge():
    assert merge([2,0,2,2]) == [4,2,0,0]
    assert merge([0,0,2,2]) == [4,0,0,0]
    assert merge([2,2,0,0]) == [4,0,0,0]
    assert merge([2,2,2,2,2]) == [4,4,2,0,0]
    assert merge([8,16,16,8]) == [8,32,8,0]
    

def test_empty_tiles():
    grid = [[1,1,5],[0,6,999]]
    empty_tiles(grid) == [(1,0)]
    
    grid = [[1,0,5],[0,6,999]]
    empty_tiles(grid) == [(0,1),(1,0)]
    
    
def test_game():
    game = TwentyFortyEight(5, 4)
    assert game._height == 5
    assert game._width == 4
    assert len(game._grid) == 5
    
    # test reset function
    not_zero_count = 0
    for i in range(5):
        row = game._grid[i]
        assert len(row) == 4
        for j in row:
            if j != 0:
                not_zero_count += 1
    assert not_zero_count == 2
    
    assert game.get_grid_height() == 5
    assert game.get_grid_width() == 4
    
    # test set_tiles, get_tiles
    game.set_tile(0,0,10)
    assert game.get_tile(0,0) == 10
    game.set_tile(3,1,4)
    assert game.get_tile(3,1) == 4
    
    # test new tiles random 90% - 2, 10% - 4
    sum_lst = []
    for _ in range(1000):
        game.reset()
        sum_lst.append(grid_sum(game._grid))
    avg = sum(sum_lst)/len(sum_lst)
    assert avg>=4 and avg <=8

    # test move function
    grid = [
        [4,2,2,2],
        [0,0,2,8],
        [4,2,2,8],
        [0,2,0,4],
    ]
    game = TwentyFortyEight(4, 4)
    setup_grid(game, grid)
    game.move(1)
    expected = [
        [8, 4, 4, 2],
        [0, 2, 2, 16],
        [0, 0, 0, 4],
        [0, 0, 0, 0],
    ]
    result = compare_grid(game._grid, expected)
    assert len(result) == 1
    
    setup_grid(game, grid)
    game.move(2)
    expected = [
        [0, 0, 0, 0],
        [0, 0, 0, 2],
        [0, 2, 2, 16],
        [8, 4, 4, 4],
    ]
    result = compare_grid(game._grid, expected)
    assert len(result) == 1
    
    setup_grid(game, grid)
    game.move(3)
    expected = [
        [4, 4, 2, 0],
        [2, 8, 0, 0],
        [4, 4, 8, 0],
        [2, 4, 0, 0],
    ]
    result = compare_grid(game._grid, expected)
    assert len(result) == 1
    
    setup_grid(game, grid)
    game.move(4)
    expected = [
        [0, 4, 2, 4],
        [0, 0, 2, 8],
        [0, 4, 4, 8],
        [0, 0, 2, 4],
    ]
    result = compare_grid(game._grid, expected)
    assert len(result) == 1
    
    # check is new tile is generated when there are changes
    game = TwentyFortyEight(2,2)
    grid = [[2,2],[0,0]]
    setup_grid(game, grid)
    game.move(1)
    assert grid_sum(game._grid) == 4
    game.move(3)
    assert grid_sum(game._grid) > 4
    
    # test direction indices mapping
    game = TwentyFortyEight(2, 3)
    assert game._dir_indices[1] == [(0,0),(0,1),(0,2)]
    assert game._dir_indices[2] == [(1,0),(1,1),(1,2)]
    assert game._dir_indices[3] == [(0,0),(1,0)]
    assert game._dir_indices[4] == [(0,2),(1,2)]
    
    # test positive in grid method
    game = TwentyFortyEight(2, 3)
    assert game.is_in_grid(-1,1) is False
    assert game.is_in_grid(0,2) is True
    assert game.is_in_grid(0,0) is True
    assert game.is_in_grid(1,2) is True
    assert game.is_in_grid(1,3) is False
        
        