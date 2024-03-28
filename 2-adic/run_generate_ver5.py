from fractions import Fraction
from itertools import islice
from functools import lru_cache


@lru_cache(maxsize=None)  # 使用缓存加速计算
def fibonacci(n):
    a, b = Fraction(0), Fraction(1)
    for _ in range(n):
        a, b = b, a + b
    return a


@lru_cache(maxsize=None)
def how_times_Ln_divided_2(ln):
    times = 0
    while ln % 2 == 0:
        ln //= 2
        times += 1
    return times


n = int(input("请输入n: "))

for i in range(n):
    # 计算常数表达式
    fib1 = fibonacci(12 * i + 3)
    fib2 = fibonacci(12 * i + 4)
    const = 4 * (12 * i + 3) - 1

    # 定义Ln数列
    Ln = (const * fib1 + 2 * (12 * i + 3) * fib2) // 5
    result = how_times_Ln_divided_2(Ln)
    print(f"第 {i + 1} 个数的2-adic为：{result}")

with open("output.txt", "w") as f:
    for i in range(n):
        # 定义Ln数列
        Ln = (
            (4 * (12 * i + 3) - 1) * fibonacci(12 * i + 3)
            + 2 * (12 * i + 3) * fibonacci((12 * i + 3) + 1)
        ) // 5
        result = how_times_Ln_divided_2(Ln)
        f.write(f"{result} ")
        i += 1
