from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from itertools import islice
from functools import lru_cache


@lru_cache(maxsize=None)
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


def calculate(i):
    # 计算常数表达式
    fib1 = fibonacci(12 * i + 3)
    fib2 = fibonaci(12 * i + 4)
    const = 4 * (12 * i + 3) - 1

    # 定义Ln数列
    Ln = (const * fib1 + 2 * (12 * i + 3) * fib2) // 5
    result = how_times_Ln_divided_2(Ln)
    print(f"第 {i} 个数的2-adic为：{result}")
    return result


n = int(input("请输入n: "))

with ThreadPoolExecutor() as executor:
    results = executor.map(calculate, range(n))

with open("output.txt", "w") as f:
    for result in results:
        f.write(f"{result} ")
