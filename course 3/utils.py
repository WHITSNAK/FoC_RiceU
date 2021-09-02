def grid_sum(grid):
    total = 0.
    for row in grid:
        for col in row:
            total += col
    return total


def compare_grid(grid1, grid2):
    diff = []
    for i, row in enumerate(grid1):
        for j, v in enumerate(row):
            v2 = grid2[i][j]
            if v2 != v:
                data = (i,j), v, v2
                diff.append(data)
    return diff


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


def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length
    """
    
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans


def gen_sorted_sequences(outcomes, length):
    """
    Function that creates all sorted sequences via gen_all_sequences
    """    
    all_sequences = gen_all_sequences(outcomes, length)
    sorted_sequences = [tuple(sorted(sequence)) for sequence in all_sequences]
    return set(sorted_sequences)
