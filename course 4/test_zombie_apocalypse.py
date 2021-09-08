import pytest
from zombie_apocalypse import Apocalypse, grids_min, create_grid, ZOMBIE, HUMAN
from poc_grid import Grid
from poc_queue import Queue


@pytest.fixture
def apo_filled():
    return Apocalypse(10, 20, [(0,0),(5,3),(2,8)], [(1,1),(2,2)], [(3,3),(5,4),(7,7)])

@pytest.fixture
def apo_empty():
    return Apocalypse(10, 20)


def test_init_without_data(apo_empty):
    apo = apo_empty
    height, width = apo.get_grid_height(), apo.get_grid_width()
    assert height == 10
    assert width == 20
    for row_i in range(height):
        for col_j in range(width):
            assert apo.is_empty(row_i, col_j)
    assert apo.num_zombies() == 0
    assert apo.num_humans() == 0


def test_init_with_data(apo_filled):
    height, width = apo_filled.get_grid_height(), apo_filled.get_grid_width()

    cnt = 0
    for row_i in range(height):
        for col_j in range(width):
            if not apo_filled.is_empty(row_i, col_j):
                cnt += 1
    assert cnt == 3
    assert apo_filled.num_zombies() == 2
    assert apo_filled.num_humans() == 3


def test_clear(apo_filled):
    apo = apo_filled
    apo.clear()

    height, width = apo.get_grid_height(), apo.get_grid_width()
    for row_i in range(height):
        for col_j in range(width):
            assert apo.is_empty(row_i, col_j)
    assert apo._zombie_list == []
    assert apo._human_list == []


@pytest.mark.parametrize(
    'obj, expected',
    [   # zombies and humans can overlap in one cell
        (Apocalypse(10, 20, None, [(1,1),(2,2)], [(1,1),(2,2)]), 2),
        (Apocalypse(10, 20, None, [(1,1),(2,2),(5,5)]), 3),
        (Apocalypse(10, 20), 0),
    ]
)
def test_num_zombies(obj, expected):
    assert obj.num_zombies() == expected


@pytest.mark.parametrize(
    'obj, expected',
    [   # zombies and humans can overlap in one cell
        (Apocalypse(10, 20, None, [(1,1),(2,2)], [(1,1),(2,2)]), 2),
        (Apocalypse(10, 20, None, None, [(1,1),(2,2),(5,5)]), 3),
        (Apocalypse(10, 20), 0),
    ]
)
def test_num_humans(obj, expected):
    assert obj.num_humans() == expected


def test_zombies_getset(apo_empty):
    apo = apo_empty
    assert apo.num_zombies() == 0

    ps = [(1,2), (5,4)]
    for p in ps:
        apo.add_zombie(p[0], p[1])
    assert apo.num_zombies() == 2

    assert [zombie for zombie in apo.zombies()] == ps


def test_humans_getset(apo_empty):
    apo = apo_empty
    assert apo.num_humans() == 0

    ps = [(1,2), (5,4)]
    for p in ps:
        apo.add_human(p[0], p[1])
    assert apo.num_humans() == 2

    assert [human for human in apo.humans()] == ps


@pytest.fixture
def apo_small_filled():
    return Apocalypse(5, 4, [(0,0),(0,2)], [(1,1),(2,2)], [(3,3),(0,3)])

def test_apo_enqueue_all_neighbors(apo_small_filled):
    apo = apo_small_filled
    que = Queue()

    apo._enqueue_all_neighbors(que, (0,0), 0)
    assert len(que) == 2
    item = que.dequeue()
    assert type(item[0]) is tuple
    assert item[1] == 0


def test_apo_move_humans(apo_small_filled):
    apo = apo_small_filled
    zombie_df = apo.compute_distance_field(ZOMBIE)
    apo.move_humans(zombie_df)
    assert apo._human_list[0] == (4,3)
    assert apo._human_list[1] == (0,3)


def test_apo_move_zombies(apo_small_filled):
    apo = apo_small_filled
    human_df = apo.compute_distance_field(HUMAN)
    apo.move_zombies(human_df)
    assert apo._zombie_list[0] == (1,2)
    assert apo._zombie_list[1] in [(2,3),(3,2)]


@pytest.mark.parametrize(
    'center, dist_expected',
    [
        ((0,1),
        [
            [20, 0, 20, 4],
            [2,1,2,3],
            [3,2,3,4],
            [4,3,4,5],
            [5,4,5,6],
        ]),
        ((1,1),
        [
            [20,1,20,3],
            [1,0,1,2],
            [2,1,2,3],
            [3,2,3,4],
            [4,3,4,5],
        ]),
    ]
)
def test_apo_simple_distance_field(center, dist_expected, apo_small_filled):
    apo = apo_small_filled
    dist = apo._simple_distance_field(center)
    assert dist == dist_expected


@pytest.fixture
def grid1():
    return [[1,1,1],[2,2,2]]

@pytest.fixture
def grid2():
    return [[2,2,2],[0,0,0]]

@pytest.fixture
def grid3():
    return [[3,3,3],[-1,-2,-3]]


def test_grids_min_2(grid1, grid2):
    assert grids_min(*[grid1, grid2]) == [[1,1,1],[0,0,0]]

def test_grids_min_1(grid1):
    assert grids_min(*[grid1]) == grid1

def test_grids_min_3(grid1, grid2, grid3):
    assert grids_min(*[grid1, grid2, grid3]) == [[1,1,1],[-1,-2,-3]]


def test_create_grid():
    assert len(create_grid(0,0)) == 0
    assert len(create_grid(0, 10)) == 0
    assert len(create_grid(10, 0)) == 0
    assert create_grid(5, 3, 10)[4][2] == 10
