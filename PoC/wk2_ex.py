# %%
def triangular_sum(num):
    if num < 0:
        raise ValueError('only [0, +oo] numbers are allowed')
    
    if num <= 1:
        return num
    
    return num + triangular_sum(num-1)

# %%
def number_of_threes(num):
    if num == 0:
        return 0
    else:
        unit_digit = num % 10
        threes_in_rest = number_of_threes(num//10)
        if unit_digit == 3:
            return threes_in_rest + 1
        else:
            return threes_in_rest
        

# %%
def is_member(my_list, elem):
    if len(my_list) == 0:
        return False

    if elem == my_list[0]:
        return True
    else:
        return is_member(my_list[1:], elem)

# %%
def remove_x(my_string):
    """
    'catxxdogx' -> 'catdog'
    """
    if my_string == '':
        return ''

    initial_letter = my_string[0]
    rest_letters_removed = remove_x(my_string[1:])
    if initial_letter == 'x':
        return rest_letters_removed
    else:
        return initial_letter + rest_letters_removed


# %%
def insert_x(my_string):
    if my_string == '':
        return ''
    else:
        initial_letter = my_string[0]
        rest_inserted = insert_x(my_string[1:])
        if rest_inserted == '':
            return initial_letter
        else:
            return initial_letter + 'x' + rest_inserted

# %%
def list_reverse(my_list):
    """[2,3,1] -> [1,3,2]"""
    if len(my_list) == 0:
        return []
    else:
        last_item = my_list[-1:]
        rest_reversed = list_reverse(my_list[:-1])
        return last_item + rest_reversed

# %%
def gcd(num1, num2):
    """Euclid Algo"""
    if num1 == 0 or num2 == 0:
        return max(num1, num2)

    if num1 == num2:
        return num1
    else:
        diff = abs(num1 - num2)
        return gcd(diff, min(num1, num2))


# %%
def slice(my_list, first, last):
    if len(my_list) == last - first:
        return my_list
    else:
        if first > 0:
            my_list.pop(0)
        else:
            my_list.pop(-1)
        return slice(my_list, first-1, last-1)
