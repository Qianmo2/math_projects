import time

from fractions import Fraction
from itertools import islice
from functools import lru_cache


def matrix_multiply(matrix1, matrix2):  # 计算两个矩阵的乘积
    """
    一个三元组(a, b, c)被用来表示一个2x2的矩阵：
    | a b | * | d e |
    | b c |   | e f |"""

    a, b, c = matrix1  # 三元组
    d, e, f = matrix2
    return a * d + b * e, a * e + b * f, b * e + c * f


def matrix_power(matrix, power):  # 返回矩阵的幂运算结果
    if power <= 0:
        return 1, 0, 0
    elif power == 1:
        return matrix
    else:
        """
        递归快速幂算法

        如果幂大于1，函数先计算矩阵的半个幂，然后判断幂是否为偶数
        如果是偶数，就返回半个幂的矩阵乘以自身的结果
        如果是奇数，就返回原矩阵乘以半个幂的矩阵乘以自身的结果

        对于任意的非零实数a和非负整数n，有以下性质：
        如果n是偶数，那么a^n = (a^(n/2))^2。例如 a^4 = (a^2)^2
        如果n是奇数，那么a^n = a * a^(n-1)。例如 a^5 = a * a^4

        最终：
        原来需要O(n)次乘法的问题，变成了O(log(n))次乘法的问题"""

        half_power = matrix_power(matrix, power // 2)
        if power % 2 == 0:
            return matrix_multiply(half_power, half_power)
        else:
            return matrix_multiply(matrix, matrix_multiply(half_power, half_power))


@lru_cache(maxsize=None)  # 使用lru_cache装饰器来缓存计算结果
def fibonacci(n):
    if n <= 0:
        return 0
    else:
        """返回矩阵幂运算结果的第一个元素

        斐波那契数列有一个性质，它可以通过一个2x2矩阵的幂运算来计算
        定义一个2x2矩阵，这个矩阵的n次幂的第一行第一列的元素就是斐波那契数列的第n+1项
        所以先计算这个矩阵的n-1次幂，然后返回结果矩阵的第一个元素
        就得到了斐波那契数列的第n项"""

        matrix = (1, 1, 0)
        powered_matrix = matrix_power(matrix, n - 1)
        return powered_matrix[0]


@lru_cache(maxsize=None)  # 使用lru_cache装饰器来缓存计算结果
def how_times_Ln_divided_2(ln):
    times = 0
    while ln % 2 == 0:
        ln //= 2
        times += 1
    return times


n = int(input("请输入n: "))

start_time = time.time()  # 开始计时

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

end_time = time.time()  # 结束计时

print(f"程序运行时间: {end_time - start_time} 秒")  # 输出运行时间
