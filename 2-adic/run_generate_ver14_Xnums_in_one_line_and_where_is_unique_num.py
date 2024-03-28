import time
import logging
import gmpy2
from multiprocessing import Pool

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()


def matrix_multiply(matrix1, matrix2):
    """
    一个三元组(a, b, c)被用来表示一个2x2的矩阵
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
        half_power_squared = matrix_multiply(half_power, half_power)
        if power % 2 == 0:
            return half_power_squared
        else:
            return matrix_multiply(matrix, half_power_squared)


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


def calculate_2adic(index):  # 核心算法，这我不懂XD
    fib1 = fibonacci(12 * index + 3)
    fib2 = fibonacci(12 * index + 4)
    const = gmpy2.mpz(4 * (12 * index + 3) - 1)
    Ln = (const * fib1 + 2 * (12 * index + 3) * fib2) // 5
    result = how_times_Ln_divided_2(Ln)
    logger.info(f"第 {index + 1} 个数的 2-adic 为：{result}")
    return result


def is_power_of_two(n):
    """
    检查一个整数是否是2的幂
    """
    return (n != 0) and (n & (n - 1) == 0)


def main(n, x):
    """
    使用p.map()并行地对range(n)中的每个数调用 calculate_2adic()
    range(n)生成从 0 到 n-1 的整数序列
    p.map()会返回一个列表，其中包含每个函数调用的结果
    """
    start_time = time.time()

    with Pool() as p:
        results = p.map(calculate_2adic, range(n))

    # 通过列表推导式将结果转换为二维数组
    # 从results列表中取出从索引i开始的x个元素作为一个新的子列表
    # range(0, len(results), x)生成一个从0开始，步长为x的序列，确保每次取出的子列表之间没有重叠
    results_matrix = [results[i : i + x] for i in range(0, len(results), x)]

    # 找出每行中唯一的数字的位置
    unique_index = None  # 存储每行中唯一的数字的位置
    for i in range(x):
        if len(set(row[i] for row in results_matrix[:2])) > 1:
            """
            set(row[i] for row in results_matrix[:2])
                集合推导式。遍历 results_matrix 的前两行，从每行中取出索引为 i 的元素
                于是得到了一个包含前两行在位置 i 的元素的集合
            if len(...) > 1
                集合不包含重复元素。
                如果前两行在位置 i 的元素相同，那么集合的长度是1
                如果不同，那么长度是2
            """
            unique_index = i
            break

    with open(f"output_{x}nums_in_one_line.txt", "w") as f:
        for row in results_matrix:  # 遍历 results_matrix 中的每一行
            f.write(
                f"总项数 = {n}    每行包含项数 = {x}    "
                f"unique_num = 第 {unique_index + 1} 位"
                f"    |    "
            )  # 在每一行的开始写入 unique_index 的值
            for i, result in enumerate(row):
                if i == unique_index:  # 检查其位置是否等于 unique_index
                    f.write(f"\t{str(result)}\t")
                else:
                    f.write(f"{str(result)} ")
            f.write("\n")

    end_time = time.time()

    logger.info(f"程序运行时间: {end_time - start_time} 秒")


if __name__ == "__main__":
    while True:
        n, x = map(int, input("请输入n和x，用空格分隔。n是要计算到多少项，x是每输出多少项换行，x一定是2的幂: ").split())
        if is_power_of_two(x):
            main(n, x)
            break
        else:
            print("输入的x不是2的幂，请重新输入。")
