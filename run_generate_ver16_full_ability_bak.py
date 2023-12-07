import time
import logging
import gmpy2
import os
import re
from multiprocessing import Pool, TimeoutError

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


def get_latest_file():
    # 获取当前目录下所有output_n={n}.txt文件，并找到n最大的文件
    files = [f for f in os.listdir(".") if re.match(r"output_n=\d+\.txt", f)]
    if not files:
        return None
    files.sort(
        key=lambda x: int(re.search(r"output_n=(\d+).txt", x).group(1)), reverse=True
    )
    return files[0]


def calculate_2adic(index):  # 核心算法，这我不懂XD
    fib1 = fibonacci(12 * index + 3)
    fib2 = fibonacci(12 * index + 4)
    const = gmpy2.mpz(4 * (12 * index + 3) - 1)
    Ln = (const * fib1 + 2 * (12 * index + 3) * fib2) // 5
    result = how_times_Ln_divided_2(Ln)
    logger.info(f"第 {index + 1} 个数的 2-adic 为：{result}")
    return result


def main(n):
    start_time = time.time()
    start_index = 0
    results = []

    # 获取最新的文件
    latest_file = get_latest_file()
    if latest_file:
        try:
            with open(latest_file, "r") as f:
                existing_results = f.read().strip().split()
                start_index = len(existing_results)
                results = list(map(int, existing_results))
                logger.info(f"已从文件 {latest_file} 中读取 {start_index} 个结果。")
        except FileNotFoundError:
            logger.info("文件不存在，将创建新文件并从头开始计算。")
    else:
        logger.info("未找到现有文件，" "将创建新文件并从头开始计算。")

    # 检查用户输入的n是否小于已计算的数量
    if n <= start_index:
        logger.info(f"文件中已包含 {start_index} 个数，无需进行更多计算。")
        output_filename = f"output_n={n}.txt"
        with open(output_filename, "w") as f:
            f.write(" ".join(map(str, results[:n])))
    else:
        # 从断点继续计算
        with Pool() as p:
            async_result = p.map_async(calculate_2adic, range(start_index, n))

            try:
                # 每隔一段时间检查一次是否完成
                while not async_result.ready():
                    async_result.wait(timeout=0.1)
                # 获取所有结果
                new_results = async_result.get()
            except KeyboardInterrupt:
                # 用户按下 Ctrl+C，获取当前已经计算的结果
                logger.info("用户中断了计算。")
                # 获取目前为止已经完成的结果
                if not async_result.ready():
                    p.terminate()
                    p.join()
                    # 使用 _value 属性时要特别小心，它可能包含 None 值
                    # 使用列表推导式过滤 None 值
                    new_results = [res for res in async_result._value if res is not None]
            finally:
                # 如果 new_results 被赋值了，则扩展 results 列表
                if 'new_results' in locals():
                    results.extend(new_results)
                # 写入到新文件 output_n={当前已计算的数量}.txt
                actual_count = len(results)
                output_filename = f"output_n={actual_count}.txt"
                with open(output_filename, "w") as f:
                    # 写入时排除 None 值
                    f.write(" ".join(map(str, [res for res in results if res is not None])))

                end_time = time.time()
                logger.info(f"程序运行时间: {end_time - start_time} 秒")
                logger.info(f"结果已写入到 {output_filename}")


if __name__ == "__main__":
    n = int(input("请输入n: "))
    main(n)