import pytest
from fifteen_puzzle import Puzzle
from fifteen_puzzle import Grid, Queue, Node, SimpleGraph
from fifteen_puzzle import create_path_graph, trace_root, path2moves


@pytest.fixture
def grid_config44():
    height, width = 4, 4
    grid = Grid(height, width)
    return grid


def test_grid(grid_config44):
    grid = grid_config44
    height, width = grid.get_grid_height(), grid.get_grid_width()

    assert grid.get_grid_height() == height
    assert grid.get_grid_width() == width

    for row_i in range(height):
        for col_j in range(width):
            assert grid.is_empty(row_i, col_j)
    
    assert grid.is_empty(2, 2)
    grid.set_full(2, 2)
    assert not grid.is_empty(2, 2)
    grid.set_empty(2, 2)
    assert grid.is_empty(2, 2)

    grid.set_full(2, 2)
    grid.set_full(2, 1)
    assert not grid.is_empty(2, 2)
    assert not grid.is_empty(2, 1)
    
    new_grid = grid.clone()
    assert new_grid is not grid
    assert not new_grid.is_empty(2, 2)
    assert not new_grid.is_empty(2, 1)

    grid.clear()
    for row_i in range(height):
        for col_j in range(width):
            assert grid.is_empty(row_i, col_j)
    
    assert grid.get_index(0) == (0, 0)
    assert grid.get_index(5) == (1, 1)
    assert grid.get_index(11) == (2, 3)

def test_grid_neighbor_full(grid_config44):
    grid = grid_config44
    neighs = grid.four_neighbors(1, 1)
    assert neighs == [(0, 1), (2, 1), (1, 0), (1, 2)]

def test_grid_neighbor_edge(grid_config44):
    grid = grid_config44
    neighs = grid.four_neighbors(0, 1)
    assert neighs == [None, (1, 1), (0, 0), (0, 2)]

def test_grid_neighbor_corner(grid_config44):
    grid = grid_config44
    neighs = grid.four_neighbors(3, 3)
    assert neighs == [(2, 3), None, (3, 2), None]

def test_queue():
    que = Queue()

    for i in range(6):
        que.enqueue(i)

    for i in range(6):
        assert que.dequeue() == i
    assert len(que) == 0

def test_node():
    node1 = Node((1,2))
    assert node1._value == (1,2)
    node2 = Node(100)
    assert node2._value == 100

    node2.set_parent(node1)
    assert node2.get_parent() == node1
    assert node1.get_child() == None

def test_graph():
    graph = SimpleGraph()
    assert len(graph) == 0

    node1 = graph.add_node((0,0))
    node2 = graph.add_node((0,1))
    node3 = graph.add_node((0,2))

    assert len(graph) == 3
    assert node1 in graph
    assert node2 in graph
    assert node3 in graph
    assert Node((0,0)) in graph
    assert Node((0,5)) not in graph

    assert graph.find_node((0,0)) is node1
    assert graph.find_node((0,5)) is None

    node_removed = graph.remove_node((0,1))
    assert node_removed is node2
    assert node2 not in graph
    assert len(graph) == 2

def test_create_path_graph_no_obstacles(grid_config44):
    grid = grid_config44
    start, target = (0,0), (2,2)
    graph, target_node = create_path_graph(grid, start, target)
    assert target_node is not None
    assert target_node == Node(target)
    assert len(graph) == 12


def test_create_path_graph_with_obstacles(grid_config44):
    grid = grid_config44
    start, target = (2,0), (0,2)
    grid.set_full(1,0)
    for num in range(10, 16):
        row_i, col_j = grid.get_index(num)
        grid.set_full(row_i, col_j)

    graph, target_node = create_path_graph(grid, start, target)
    
    assert len(graph) == 7
    assert target_node == Node(target)

def test_create_path_graph_not_reachable(grid_config44):
    grid = grid_config44
    start, target = (2,0), (0,2)
    grid.set_full(1,0)
    grid.set_full(0,1)
    grid.set_full(1,2)
    for num in range(10, 16):
        row_i, col_j = grid.get_index(num)
        grid.set_full(row_i, col_j)

    graph, target_node = create_path_graph(grid, start, target)
    
    assert target_node is None
    assert len(graph) == 3

def test_trace_root():
    node1 = Node((0,0))
    node2 = Node((0,1))
    node2.set_parent(node1)
    node3 = Node((1,1))
    node3.set_parent(node2)

    trace = trace_root(node3, trace=[])
    assert len(trace) == 3
    assert trace[0] is node1
    assert trace[-1] is node3

def test_trace_root_self():
    node1 = Node((0,0))
    trace = trace_root(node1, trace=[])
    assert len(trace) == 1
    assert trace[0] is node1


@pytest.mark.parametrize(
    'path, expected',
    [
        ([Node((0,0)), Node((0,1)), Node((0,2)), Node((0,1))], 'rrl'),
        ([Node((0,0)), Node((1,0)), Node((2,0))], 'dd'),
        ([Node((5,1)), Node((4,1)), Node((4,2)), Node((3,2)), Node((4,2))], 'urud'),
    ],
)
def test_path2moves(path, expected):
    assert path2moves(path) == expected


@pytest.fixture
def puzzle_44config1():
    _config = [
        [ 2, 4, 6, 5],
        [ 1,10, 3, 7],
        [ 8, 9, 0,11],
        [12,13,14,15],
    ]
    return Puzzle(4,4,_config)

@pytest.fixture
def puzzle_44config2():
    _config = [
        [ 4, 1, 7, 2],
        [ 8, 6, 9, 3],
        [ 5, 0,10,11],
        [12,13,14,15],
    ]
    return Puzzle(4,4,_config)

@pytest.fixture
def puzzle_44config3():
    _config = [
        [ 1, 2, 6, 3],
        [ 4, 5,11,10],
        [ 8, 0, 9, 7],
        [12,13,14,15],
    ]
    return Puzzle(4,4,_config)

@pytest.fixture
def puzzle_44config4():
    _config = [
        [ 8, 1, 2, 3],
        [ 9, 6, 4, 7],
        [ 5,11,10, 0],
        [12,13,14,15],
    ]
    return Puzzle(4,4,_config)

@pytest.fixture
def puzzle_44config5():
    _config = [
        [ 1, 8, 2, 3],
        [ 5, 6, 4, 7],
        [ 0, 9,10,11],
        [12,13,14,15],
    ]
    return Puzzle(4,4,_config)


@pytest.fixture
def puzzle_44config6():
    _config = [
        [ 8, 1, 2, 3],
        [ 5, 6, 4, 7],
        [15, 9,10,11],
        [12,13,14, 0],
    ]
    return Puzzle(4,4,_config)


def test_lower_row_invariant1(puzzle_44config1):
    puzzle = puzzle_44config1
    assert puzzle.lower_row_invariant(2,2)
    assert not puzzle.lower_row_invariant(2,1)

def test_lower_row_invariant2(puzzle_44config2):
    puzzle = puzzle_44config2
    assert puzzle.lower_row_invariant(2,1)
    assert not puzzle.lower_row_invariant(1,1)

def test_lower_row_invariant_bad_zero(puzzle_44config3):
    puzzle = puzzle_44config3
    assert not puzzle.lower_row_invariant(2,1)
    assert not puzzle.lower_row_invariant(2,3)

def test_lower_row_invariant_edge_right(puzzle_44config4):
    puzzle = puzzle_44config4
    assert puzzle.lower_row_invariant(2,3)
    assert not puzzle.lower_row_invariant(2,2)

def test_lower_row_invariant_edge_left(puzzle_44config5):
    puzzle = puzzle_44config5
    assert puzzle.lower_row_invariant(2,0)
    assert not puzzle.lower_row_invariant(2,1)

def test_lower_row_invariant_none(puzzle_44config6):
    puzzle = puzzle_44config6
    assert puzzle.lower_row_invariant(3,3)
    assert not puzzle.lower_row_invariant(2,1)


# def test_solve_interior_tile1(puzzle_44config1):
#     puzzle = puzzle_44config1
#     assert puzzle.solve_interior_tile() == 'uldruld'