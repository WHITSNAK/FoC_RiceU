"""
Merge function for 2048 game.
"""

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


print merge([2,0,2,2]) == [4,2,0,0]
print merge([0,0,2,2]) == [4,0,0,0]
print merge([2,2,0,0]) == [4,0,0,0]
print merge([2,2,2,2,2]) == [4,4,2,0,0]
print merge([8,16,16,8]) == [8,32,8,0]
