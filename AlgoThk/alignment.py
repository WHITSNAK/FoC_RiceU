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


def _matrix_max(matrix):
    """Finds the max value in a matrix along its indexes"""
    max_val = float('-inf')
    max_i, max_j = None, None

    for row_i, row in enumerate(matrix):
        for col_j, tile in enumerate(row):
            if tile > max_val:
                max_val = tile
                max_i, max_j = row_i, col_j
    
    return max_val, max_i, max_j


def _compute_alignment(seq_x, seq_y, scores, aligns, kind='global'):
    """Internal alignment finding function"""
    # start with empty sequences
    _x2, _y2 = '', ''

    # init the starting tile
    if kind == 'global':
        row_i, col_j = len(seq_x), len(seq_y)
        score = aligns[row_i][col_j]
    elif kind == 'local':
        score, row_i, col_j = _matrix_max(aligns)

    # traverse and creating the subsequence alone the DP table
    while row_i != 0 and col_j != 0:
        _align = aligns[row_i][col_j]
        if kind == 'local' and _align == 0:
            # early terminate when encounter the first zero
            break

        if _align == aligns[row_i-1][col_j-1] + scores[seq_x[row_i-1]][seq_y[col_j-1]]:
            _x2 = seq_x[row_i-1] + _x2
            _y2 = seq_y[col_j-1] + _y2
            row_i -= 1
            col_j -=1
        elif _align == aligns[row_i-1][col_j] + scores[seq_x[row_i-1]]['-']:
            _x2 = seq_x[row_i-1] + _x2
            _y2 = '-' + _y2
            row_i -= 1
        else:
            _x2 = '-' + _x2
            _y2 = seq_y[col_j-1] + _y2
            col_j -= 1
    
    # pad in the remaing, only for global alignment
    if kind == 'global':
        while row_i != 0:
            _x2 = seq_x[row_i-1] + _x2
            _y2 = '-' + _y2
            row_i -= 1
        
        while col_j != 0:
            _x2 = '-' + _x2
            _y2 = seq_y[col_j-1] + _y2
            col_j -= 1
    
    return score, _x2, _y2


def compute_global_alignment(seq_x, seq_y, scores, aligns):
    """
    Finds the optimal global alignment of two given sequences

    parameter
    ---------
    seq_x, seq_y: two sequences used to look for a global alignment
    scores: scoring matrix that is used in alignments
    aligns: the DP matrix for all alignments

    return
    ------
    (score, X', Y'): tuple
        the optimal score, and two globally aligned sequences with the same size
        '-' might be added
    
    example
    -------
    X = 'AA', Y = 'TAAT'
    >> (8, '-AA-', 'TAAT')
    """
    return _compute_alignment(seq_x, seq_y, scores, aligns, kind='global')


def compute_local_alignment(seq_x, seq_y, scores, aligns):
    """
    Finds the optimal local alignment of two given sequences

    parameter
    ---------
    seq_x, seq_y: two sequences used to look for a local alignment
    scores: scoring matrix that is used in alignments
    aligns: the DP matrix for all alignments

    return
    ------
    (score, X', Y'): tuple
        the optimal score, and two locally aligned sub-sequences with the same size
        '-' might be added
    
    example
    -------
    X = 'AA', Y = 'TAAT'
    >> (20, 'AA', 'AA')
    """
    return _compute_alignment(seq_x, seq_y, scores, aligns, kind='local')

