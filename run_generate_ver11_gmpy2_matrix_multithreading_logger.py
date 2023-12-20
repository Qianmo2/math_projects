import time
import logging
import gmpy2
from fractions import Fraction
from itertools import islice
from functools import lru_cache
import concurrent.futures

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()

"""
lru_cache是Python的内置装饰器，用于实现最近最少使用（LRU）的缓存策略
当装饰的函数被调用时lru_cache会检查缓存中是否已经有了这个函数调用的结果
如果有，它就直接返回缓存的结果，而不需要再次执行函数的代码
如果没有，它就会执行函数的代码，然后将结果存入缓存

这样，当函数被频繁调用时，可以避免重复计算，从而提高效率。
本实例中lru_cache装饰器的maxsize参数被设置为None，表示缓存的大小没有限制
"""


# 计算两个矩阵的乘积
def matrix_multiply(matrix1, matrix2):
    """
    一个三元组(a, b, c)被用来表示一个2x2的矩阵：
    | a b | * | d e |
    | b c |   | e f |
    """
    a, b, c = matrix1
    d, e, f = matrix2
    return (
        gmpy2.mul(a, d) + gmpy2.mul(b, e),
        gmpy2.mul(a, e) + gmpy2.mul(b, f),
        gmpy2.mul(b, e) + gmpy2.mul(c, f),
    )


# 返回矩阵的幂运算结果
def matrix_power(matrix, power):
    """
    递归快速幂算法

    如果幂大于1，函数先计算矩阵的半个幂，然后判断幂是否为偶数
    如果是偶数，就返回半个幂的矩阵乘以自身的结果
    如果是奇数，就返回原矩阵乘以半个幂的矩阵乘以自身的结果

    对于任意的非零实数a和非负整数n，有以下性质：
    如果n是偶数，那么a^n = (a^(n/2))^2。例如 a^4 = (a^2)^2
    如果n是奇数，那么a^n = a * a^(n-1)。例如 a^5 = a * a^4

    最终：
    原来需要O(n)次乘法的问题，变成了O(log(n))次乘法的问题
    """

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
    """
    斐波那契数列有一个性质，它可以通过一个2x2矩阵的幂运算来计算
    这个矩阵的n次幂的第一行第一列的元素就是斐波那契数列的第n+1项
    所以先计算这个矩阵的n-1次幂，然后返回结果矩阵的第一个元素
    就得到了斐波那契数列的第n项

    F(n) = F(n-1) + F(n-2)
    等效于
    | F(n)   |   =   | 1 1 | * | F(n-1) |
    | F(n-1) |       | 1 0 |   | F(n-2) |

    又powered_matrix =
    | powered_matrix[0], powered_matrix[1] |
    | powered_matrix[1], powered_matrix[2] |
    """

    if n <= 0:
        return gmpy2.mpz(0)
    else:
        matrix = (gmpy2.mpz(1), gmpy2.mpz(1), gmpy2.mpz(0))
        powered_matrix = matrix_power(matrix, n - 1)
        return powered_matrix[0]


# 使用lru_cache装饰器来缓存计算结果
@lru_cache(maxsize=None)
def how_times_Ln_divided_2(ln):
    times = 0
    bit_length = ln.bit_length()  # 获取ln的二进制位长度
    while bit_length > 0:
        if ln.is_even():  # 检查ln是否为偶数
            ln = gmpy2.f_div_2exp(ln, 1)  # ln除以 2，函数的第二个参数是除数的指数
            times += 1
        else:
            break
        bit_length -= 1  # 二进制位长度减1
    return times


# 并行计算的函数，包括打印语句
def calculate_2adic(index):  # 核心算法，这我不懂XD
    fib1 = fibonacci(12 * index + 3)
    fib2 = fibonacci(12 * index + 4)
    # 使用gmpy2的mpz类型
    const = gmpy2.mpz(4 * (12 * index + 3) - 1)
    Ln = (const * fib1 + 2 * (12 * index + 3) * fib2) // 5
    result = how_times_Ln_divided_2(Ln)
    logger.info(f"第 {index + 1} 个数的 2-adic 为：{result}")
    return result


def main(n):
    start_time = time.time()  # 记录开始时间

    """
    用with语句创建一个ProcessPoolExecutor的上下文管理器，代码块执行完毕后，进程池会自动关闭释放资源
    executor.map()函数返回一个迭代器，将迭代器转换为列表，可以得到一个包含前n个数的2-adic值的列表，赋results

    with concurrent.futures.ProcessPoolExecutor() as executor: 
        用concurrent.futures.ProcessPoolExecutor()类创建一个进程池，实现并行计算，根据CPU核心创建相应数量的进程

    results = list(executor.map(calculate_2adic, range(n)))
        用executor.map()函数将calculate_2adic函数应用到range(n)中的每个元素上
        range(n)生成一个从 0 到 n - 1 的整数序列
        executor.map()函数将这个序列中的每个元素作为参数传递给calculate_2adic函数，并在进程池中并行执行这些函数调用
        executor.map()函数返回一个迭代器，其中包含所有函数调用的结果，这些结果按照range(n)中元素的顺序排列
    """

    with concurrent.futures.ProcessPoolExecutor() as executor:
        # 用executor.map()函数并行计算每个index的2-adic值
        # index 是从 0 到 n - 1
        results = list(executor.map(calculate_2adic, range(n)))

    with open("output_all_num.txt", "w") as f:
        # 将 results 中的所有元素转换为字符串，然后用空格连接
        f.write(" ".join(map(str, results)))

    end_time = time.time()  # 记录结束时间

    # 计算并输出程序的运行时间
    logger.info(f"程序运行时间: {end_time - start_time} 秒")


if __name__ == "__main__":
    n = int(input("请输入n: "))
    main(n)
