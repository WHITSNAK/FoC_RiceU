import math


def count_inversion(lst):
    """
    MergeSort version of Inversion counter

    inversion def
    -------------
    for index i, j in lst
    a inversion is <- i<j and lst[i] > lst[j]
    """
    if len(lst) <= 1:
        return 0
    
    # split down to two subproblems
    mid = len(lst) // 2
    lst_b = lst[:mid]
    lst_c = lst[mid:]

    # recursion
    il = count_inversion(lst_b)
    ir = count_inversion(lst_c)
    im = merge(lst_b, lst_c, lst)
    return il + ir + im


def merge(lst_b, lst_c, lst_a):
    """Inplace mergesort on one recursion"""
    count = 0
    i, j, k = 0, 0, 0
    len_p, len_q = len(lst_b), len(lst_c)

    while i < len_p and j < len_q:
        # update the respect index
        if lst_b[i] <= lst_c[j]:
            lst_a[k] = lst_b[i]
            i += 1
        else:
            lst_a[k] = lst_c[j]
            j += 1

            # how many items in p moved heads
            # equals the number of inversion
            count += len_p - i
        k += 1

    # update the remaining all together
    if i == len_p:
        for idx in range(j, len_q):
            lst_a[k+idx-j] = lst_c[idx]
    else:
        for idx in range(i, len_p):
            lst_a[k+idx-i] = lst_b[idx]
        
    return count


