"""
Word Wrangler game
"""
# %%
import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists
def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    """
    if len(list1) == 0:
        return list1

    # initalize
    last_item = list1[0]
    new_lst = [last_item]
    for item in list1[1:]:
        # if the same, ignore
        if item == last_item:
            continue
        
        # if not, update and add
        new_lst.append(item)
        last_item = item
    return new_lst

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.
    """
    new_lst = []
    lst1, lst2 = remove_duplicates(list1), remove_duplicates(list2)

    while len(lst1) != 0 and len(lst2) != 0:
        # 3 cases in total
        if lst1[0] < lst2[0]:
            lst1.pop(0)
        elif lst1[0] == lst2[0]:
            item = lst1.pop(0)
            _ = lst2.pop(0)
            new_lst.append(item)
        else:
            lst2.pop(0)
    return new_lst

# Functions to perform merge sort
def merge(list1, list2):
    """
    Merge two sorted lists.

    parameter
    ---------
    list1, list2: two ascendingly sorted lists

    return
    ------
    a new sorted list containing those elements that are in
    either list1 or list2.

    note: iterative implementation
    """
    # no need to merge
    if len(list1) == 0 or len(list2) == 0:
        return list1 + list2

    new_lst = []
    lst1, lst2 = list(list1), list(list2)
    
    # stops when either the list is exhuasted
    while len(lst1) != 0 and len(lst2) != 0:
        # 3 cases in total
        if lst1[0] < lst2[0]:
            new_lst.append(lst1.pop(0))
        elif lst1[0] == lst2[0]:
            new_lst.extend([lst1.pop(0), lst2.pop(0)])
        else:
            new_lst.append(lst2.pop(0))

    # the remaing has to greater than the new_lst
    # adding [] does not change the result
    return new_lst + lst1 + lst2
                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    # base case
    if len(list1) == 0:
        return []

    mid_i = len(list1) // 2
    pivot = list1[mid_i]
    lesser, pivots, greater = [], [], []
    for item in list1:
        if item < pivot:
            lesser.append(item)
        elif item == pivot:
            pivots.append(item)
        else:
            greater.append(item)
    return merge_sort(lesser) + pivots + merge_sort(greater)

# Function to generate all strings for the word wrangler game
def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters
    in a word in any order.

    parameter
    ---------
    word: str, a word to make bunches of other words

    return
    ------
    a list of all strings that can be formed from the letters
    in the word provided.
    
    note: recursive implementation
    math: the # of items = sum of nPk, for k=0 to n, where n = len(word)
    """
    # base case
    if len(word) == 0:
        return ['']
    
    new_lst = []
    first_l = word[0]
    rest_strings = gen_all_strings(word[1:])
    for string in rest_strings:
        # add the letter in all possible locations
        for idx in range(len(string)+1):
            new_lst.append(string[:idx] + first_l + string[idx:])
    
    # concate all recursive cases
    return rest_strings + new_lst

# Function to load words from a file
def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    result = [line[:-1] for line in netfile.readlines()]
    return result

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()

    