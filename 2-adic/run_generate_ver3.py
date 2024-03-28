import numpy as np


def f(n):
    fib = np.arange(n + 1, dtype=np.int64)  # 使用numpy数组存储结果
    fib[0] = 0
    1
    for i in range(2, n + 1):
        fib[i] = np.power(fib[i - 1], 1) + np.power(fib[i - 2], 1)
    return fib[n]


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
