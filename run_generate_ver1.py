def f(n):
    if n <= 0:
        return 0
    if n == 1:
        return 1
    return f(n - 1) + f(n - 2)


def m1(y):
    n = 0
    while y % 2 == 0:
        y = y // 2
        n += 1
    return n


m = 2
r = 4
t = 12
i = 0
o = 1
p = 3

n = int(input("请输入n："))
while i <= n:
    Ln = (
        (r * (t * i + p) - 1) * f(t * i + p) + m * (t * i + p) * f((t * i + p) + 1)
    ) // 5
    v = m1(Ln)
    print("第{}个数的2-adic为：{}".format(i, v))
    i = i + o
