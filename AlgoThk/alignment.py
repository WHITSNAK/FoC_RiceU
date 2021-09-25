"""
Module for computing global and local alignment
of two strings
"""

# %%
def build_scoring_matrix(alph, diag_s, odiag_s, dash_s):
    """
    Build a scoring matrix that is used in alignment problem
        in 2-D space

    parameter
    ---------
    alph: a set of alphabets, '-' dash will be included if not there
    diag_s: diagonal score, same alphabets
    odiag_s: off diagonal score, different alphabets
    dash_d: score for any pair with a '-'

    return
    ------
    2-D Symetric scoring matrix in the form of dict of dicts
        scores for '-' are always located on last row and column
    """
    # append dash if not here
    _alph = sorted(alph)
    if '-' not in _alph:
        _alph += ['-']
    
    matrix = {}
    for row_c in _alph:
        row = {}
        for col_c in _alph:
            if '-' == row_c or '-' == col_c:
                row[col_c] = dash_s
            elif row_c == col_c:
                row[col_c] = diag_s
            else:
                row[col_c] = odiag_s
        matrix[row_c] = row
    return matrix


def create_matrix(nrow, ncol, default=0):
    """Creates a matrix in the form of a list of lists with default value"""
    matrix = []
    for _ in range(nrow):
        row = [default for _ in range(ncol)]
        matrix.append(row)
    return matrix


def _zero_floor(val, flag):
    """
    Quick helper function that keeps number min to zero
        while the flag is on/True
    """
    if flag and val < 0:
        return 0
    return val


def compute_alignment_matrix(seq_x, seq_y, scores, global_flag):
    """
    Build the alignment score matrix with the given two sequences
        in 2-D space. It is the same as dynamic programming matrix
        that is used to traverse back to find the optimal soultion.

    parameter
    ---------
    seq_x, seq_y: str, two string sequences used for computing alignment matrix
    scores: matrix, scoring matrix with shape (x+1, y+1)
    global_flag: True for global alignment, False for local alignment

    return
    ------
    alignment matrix with shape (x+1, y+1)
    """
    len_x, len_y = len(seq_x), len(seq_y)

    # init matrix
    matrix = create_matrix(len_x+1, len_y+1, 0)
    for idx_i in range(1, len_x+1):
        val = matrix[idx_i-1][0] + scores[seq_x[idx_i-1]]['-']
        matrix[idx_i][0] = _zero_floor(val, not global_flag)
    for idx_j in range(1, len_y+1):
        val = matrix[0][idx_j-1] + scores['-'][seq_y[idx_j-1]]
        matrix[0][idx_j] = _zero_floor(val, not global_flag)

    # work way through the matrix to the bottom right corner
    for row_i in range(1, len_x+1):
        for col_j in range(1, len_y+1):
            val = max(
                matrix[row_i-1][col_j] + scores[seq_x[row_i-1]]['-'],  # top tile
                matrix[row_i-1][col_j-1] + scores[seq_x[row_i-1]][seq_y[col_j-1]],  # upper-left tile
                matrix[row_i][col_j-1] + scores['-'][seq_y[col_j-1]],  # left tile
            )
            matrix[row_i][col_j] = _zero_floor(val, not global_flag)

    return matrix
