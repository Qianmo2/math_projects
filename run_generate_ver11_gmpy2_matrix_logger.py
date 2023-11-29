import time
import gmpy2
import logging
from fractions import Fraction
from itertools import islice
from functools import lru_cache


# 配置日志
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()


# 计算两个矩阵的乘积
def matrix_multiply(matrix1, matrix2):
    a, b, c = matrix1
    d, e, f = matrix2
    return (
        gmpy2.mul(a, d) + gmpy2.mul(b, e),
        gmpy2.mul(a, e) + gmpy2.mul(b, f),
        gmpy2.mul(b, e) + gmpy2.mul(c, f),
    )


# 返回矩阵的幂运算结果
def matrix_power(matrix, power):
    if power <= 0:
        return 1, 0, 0
    elif power == 1:
        return matrix
    else:
        half_power = matrix_power(matrix, power // 2)
        if power % 2 == 0:
            return matrix_multiply(half_power, half_power)
        else:
            return matrix_multiply(matrix, matrix_multiply(half_power, half_power))


# 使用lru_cache装饰器来缓存计算结果
@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 0:
        return 0
    else:
        matrix = (1, 1, 0)
        powered_matrix = matrix_power(matrix, n - 1)
        return powered_matrix[0]


# 使用lru_cache装饰器来缓存计算结果
@lru_cache(maxsize=None)
def how_times_Ln_divided_2(ln):
    times = 0
    while ln & 1 == 0:  # 使用位与运算符检查最低位是否为0，即是否为偶数
        ln >>= 1  # 使用右移位运算符代替除以2
        times += 1
    return times


n = int(input("请输入n: "))

start_time = time.time()

results = []

for i in range(n):
    fib1 = fibonacci(12 * i + 3)
    fib2 = fibonacci(12 * i + 4)
    const = 4 * (12 * i + 3) - 1

    Ln = (gmpy2.mul(const, fib1) + gmpy2.mul(2 * (12 * i + 3), fib2)) // 5
    result = how_times_Ln_divided_2(Ln)
    results.append(result)
    logger.info(f"第 {i + 1} 个数的 2-adic 为：{result}")

with open("output.txt", "w") as f:
    f.write(" ".join(map(str, results)))

end_time = time.time()

logger.info(f"程序运行时间: {end_time - start_time} 秒")
