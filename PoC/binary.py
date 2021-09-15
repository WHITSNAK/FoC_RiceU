# %%
def make_binary(length):
    """Create a list of ascending binary numbers"""
    if length == 0:
        return ['']
    
    prev_binary = make_binary(length - 1)
    new_binary = []
    for binary in prev_binary:
        new_binary.append(binary + '0')
        new_binary.append(binary + '1')
    return new_binary

def make_gray(length):
    """Create a list of ascending gray code numbers"""
    if length == 0:
        return ['']

    prev_binary = make_gray(length-1)
    ref_binary = reversed(prev_binary)
    gray_code = []
    for binary in prev_binary: # first half
        gray_code.append('0' + binary)
    for binary in ref_binary: # second half on reflected
        gray_code.append('1' + binary)
    return gray_code


def bin_to_dec(bin_num):
    """Convert binary back to decimal"""
    length = len(bin_num)
    if length == 0:
        return 0

    first_digit = bin_num[0]
    rest_digits = bin_num[1:]
    if first_digit == '1':
        return 2**(length-1) + bin_to_dec(rest_digits)
    else:
        return bin_to_dec(rest_digits)
            

def gray_to_bin(gray_code):
    """Convert gray code to binary"""
    if len(gray_code) <= 1:
        return gray_code

    first_digit = gray_code[0]
    rest_digits = gray_code[1:]
    if first_digit == '1':
        second_digit = str(1 - int(rest_digits[0]))  # flip the right-adjacent digit
        rest_digits = second_digit + rest_digits[1:]
    
    return first_digit + gray_to_bin(rest_digits)

# tests
N = 10
bins = make_binary(N)
grays = make_gray(N)
for i in range(len(bins)):
    b, g = bins[i], grays[i]
    g2b = gray_to_bin(g)
    if b != g2b:
        print 'Binary', b, 'Decimal', bin_to_dec(b)
        print 'Gray Code', g, 'Back to Binary', gray_to_bin(g)
