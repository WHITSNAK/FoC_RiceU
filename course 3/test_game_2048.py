# unittests
import poc_simpletest, random

# test helper functions
def grid_sum(grid):
    total = 0.
    for row in grid:
        for col in row:
            total += col
    return total

def setup_grid(game, grid):
    game.reset()
    for i, row in enumerate(grid):
        for j, v in enumerate(row):
            game.set_tile(i, j, v)

def compare_grid(grid1, grid2):
    diff = []
    for i, row in enumerate(grid1):
        for j, v in enumerate(row):
            v2 = grid2[i][j]
            if v2 != v:
                data = (i,j), v, v2
                diff.append(data)
    return diff

# tests
def test_merge(func):
    suite = poc_simpletest.TestSuite()
    
    suite.run_test(func([2,0,2,2]), [4,2,0,0], 'Test 1')
    suite.run_test(func([0,0,2,2]), [4,0,0,0], 'Test 2')
    suite.run_test(func([2,2,0,0]), [4,0,0,0], 'Test 3')
    suite.run_test(func([2,2,2,2,2]), [4,4,2,0,0], 'Test 4')
    suite.run_test(func([8,16,16,8]), [8,32,8,0], 'Test 5')
    
    suite.report_results()
    

def test_empty_tiles(func):
    suite = poc_simpletest.TestSuite()
    
    grid = [[1,1,5],[0,6,999]]
    suite.run_test(func(grid), [(1,0)], 'Test 1')
    
    grid = [[1,0,5],[0,6,999]]
    suite.run_test(func(grid), [(0,1),(1,0)], 'Test 2')
    
    suite.report_results()
    
    
def test_game(game_class):
    suite = poc_simpletest.TestSuite()
    
    game = game_class(5, 4)
    suite.run_test(game._height, 5, 'Test 1.1')
    suite.run_test(game._width, 4, 'Test 1.2')
    suite.run_test(len(game._grid), 5, 'Test 1.3')
    
    # test reset function
    not_zero_count = 0
    for i in range(5):
        row = game._grid[i]
        suite.run_test(len(row), 4, 'Test 1.4.{}'.format(i))
        for j in row:
            if j != 0:
                not_zero_count += 1
    suite.run_test(not_zero_count, 2, 'Test 1.5')
    
    suite.run_test(game.get_grid_height(), 5, 'Test 2.1')
    suite.run_test(game.get_grid_width(), 4, 'Test 2.2')
    
    # test set_tiles, get_tiles
    game.set_tile(0,0,10)
    suite.run_test(game.get_tile(0,0), 10, 'Test 3.1')
    game.set_tile(3,1,4)
    suite.run_test(game.get_tile(3,1), 4, 'Test 3.2')
    
    # test new tiles random 90% - 2, 10% - 4
    sum_lst = []
    for _ in range(1000):
        game.reset()
        sum_lst.append(grid_sum(game._grid))
    avg = sum(sum_lst)/len(sum_lst)
    suite.run_test(avg>=4 and avg <=8, True, 'Test 3.3')
    
    # test move function

    
    grid = [
        [4,2,2,2],
        [0,0,2,8],
        [4,2,2,8],
        [0,2,0,4],
    ]
    game = game_class(4, 4)
    setup_grid(game, grid)
    game.move(1)
    expected = [
        [8, 4, 4, 2],
        [0, 2, 2, 16],
        [0, 0, 0, 4],
        [0, 0, 0, 0],
    ]
    result = compare_grid(game._grid, expected)
    suite.run_test(len(result), 1, 'Test 4.1')
    
    setup_grid(game, grid)
    game.move(2)
    expected = [
        [0, 0, 0, 0],
        [0, 0, 0, 2],
        [0, 2, 2, 16],
        [8, 4, 4, 4],
    ]
    result = compare_grid(game._grid, expected)
    suite.run_test(len(result), 1, 'Test 4.2')
    
    setup_grid(game, grid)
    game.move(3)
    expected = [
        [4, 4, 2, 0],
        [2, 8, 0, 0],
        [4, 4, 8, 0],
        [2, 4, 0, 0],
    ]
    result = compare_grid(game._grid, expected)
    suite.run_test(len(result), 1, 'Test 4.3')
    
    setup_grid(game, grid)
    game.move(4)
    expected = [
        [0, 4, 2, 4],
        [0, 0, 2, 8],
        [0, 4, 4, 8],
        [0, 0, 2, 4],
    ]
    result = compare_grid(game._grid, expected)
    suite.run_test(len(result), 1, 'Test 4.4')
    
    # check is new tile is generated when there are changes
    game = game_class(2,2)
    grid = [[2,2],[0,0]]
    setup_grid(game, grid)
    game.move(1)
    suite.run_test(grid_sum(game._grid)==4, True, 'Test 4.5')
    game.move(3)
    suite.run_test(grid_sum(game._grid)>4, True, 'Test 4.6')
    
    # test direction indices mapping
    game = game_class(2, 3)
    suite.run_test(game._dir_indices[1], [(0,0),(0,1),(0,2)], 'Test 5.1')
    suite.run_test(game._dir_indices[2], [(1,0),(1,1),(1,2)], 'Test 5.2')
    suite.run_test(game._dir_indices[3], [(0,0),(1,0)], 'Test 5.3')
    suite.run_test(game._dir_indices[4], [(0,2),(1,2)], 'Test 5.4')
    
    # test positive in grid method
    game = game_class(2, 3)
    suite.run_test(game.is_in_grid(-1,1), False, 'Test 6.1')
    suite.run_test(game.is_in_grid(0,2), True, 'Test 6.2')
    suite.run_test(game.is_in_grid(0,0), True, 'Test 6.3')
    suite.run_test(game.is_in_grid(1,2), True, 'Test 6.4')
    suite.run_test(game.is_in_grid(1,3), False, 'Test 6.5')
    
    suite.report_results()

        
        
        