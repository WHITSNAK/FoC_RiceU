# %%
cnt = 0

def fib(num):
    global cnt
    cnt += 1
    if num == 0:
        return 0
    elif num == 1:
        return 1
    else:
        return fib(num - 1) + fib(num - 2)

def memoized_fib(num, memo_dict):
    global cnt
    cnt += 1
    if num in memo_dict:
        return memo_dict[num]
    else:
        sum1 = memoized_fib(num - 1, memo_dict)
        sum2 = memoized_fib(num - 2, memo_dict)
        memo_dict[num] = sum1 + sum2
        return sum1 + sum2

for n in range(15):
    cnt = 0
    # print '#:', n, 'result:', memoized_fib(n, {0:0, 1:1}), 'count:', cnt
    print '#:', n, 'result:', fib(n), 'count:', cnt