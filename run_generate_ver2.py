def f(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 0:
        return 0
    if n == 1:
        return 1
    memo[n] = f(n - 1, memo) + f(n - 2, memo)
    return memo[n]


def m1(y):
    n = 0
    while y % 2 == 0:
        y = y / 2
        n += 1
    return n


m = 2
r = 4
i = 1
n = int(input("请输入n: "))
while i <= n:
    Ln = ((r * i - 1) * f(i) + m * i * f(i + 1)) / 5
    v = m1(Ln)
    print(f"第{i}个数的2-adic为： {v}")
    i += 1
