def nth_fib_num(n):
    if n == 0 | n == 1:
        m = 0
    else:
        m = nth_fib_num(n - 1) + nth_fib_num(n - 2)
    return m

n = 10
while n < 15:
    nth_fib_num(n)