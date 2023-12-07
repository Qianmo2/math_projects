import time
import logging
import gmpy2
import os
import re
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
        return matrix_multiply(matrix, half_power_squared) if power % 2 else half_power_squared


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
    while ln > 0 and ln.is_even():  # 检查ln是否为偶数
        ln = gmpy2.f_div_2exp(ln, 1)
        times += 1
    return times


def get_latest_file():
    # 获取当前目录下所有output_n={n}.txt文件，并找到n最大的文件
    files = [f for f in os.listdir(".") if re.match(r"output_n=\d+\.txt", f)]
    if not files:
        return None
    return max(files, key=lambda x: int(re.search(r"output_n=(\d+).txt", x).group(1)))


def calculate_2adic(index):  # 核心算法，这我不懂XD
    fib1 = fibonacci(12 * index + 3)
    fib2 = fibonacci(12 * index + 4)
    const = gmpy2.mpz(4 * (12 * index + 3) - 1)
    Ln = (const * fib1 + 2 * (12 * index + 3) * fib2) // 5
    result = how_times_Ln_divided_2(Ln)
    logger.info(f"第 {index + 1} 个数的 2-adic 为：{result}")
    return result


def read_existing_results(file_path):
    with open(file_path, "r") as f:
        return list(map(int, f.read().strip().split()))


def write_results_to_file(file_path, results):
    with open(file_path, "w") as f:
        f.write(" ".join(map(str, results)))


def get_latest_file_path():
    files = [f for f in os.listdir(".") if re.match(r"output_n=\d+\.txt", f)]
    if not files:
        return None
    return max(files, key=lambda x: int(re.search(r"output_n=(\d+).txt", x).group(1)))


def calculate_results(pool, start_index, end_index):
    return [pool.apply_async(calculate_2adic, args=(i,)) for i in range(start_index, end_index)]


def collect_results(result_objects):
    return [obj.get() for obj in result_objects if obj.ready()]


def main(n):
    start_time = time.time()
    latest_file_path = get_latest_file_path()
    start_index = 0
    results = []

    if latest_file_path:
        try:
            results = read_existing_results(latest_file_path)
            start_index = len(results)
            logger.info(f"已从文件 {latest_file_path} 中读取 {start_index} 个结果。")
        except FileNotFoundError:
            logger.info("文件不存在，将创建新文件并从头开始计算。")
    else:
        logger.info("未找到现有文件，将创建新文件并从头开始计算。")

    if n <= start_index:
        logger.info(f"文件中已包含 {start_index} 个数，无需进行更多计算。")
        output_filename = f"output_n={n}.txt"
        write_results_to_file(output_filename, results[:n])
    else:
        with Pool() as pool:
            result_objects = calculate_results(pool, start_index, n)
            pool.close()
            try:
                while not all(obj.ready() for obj in result_objects):
                    time.sleep(0.1)
            except KeyboardInterrupt:
                logger.info("用户中断了计算。正在保存当前结果...")
                pool.terminate()
            finally:
                pool.join()
                results.extend(collect_results(result_objects))
                output_filename = f"output_n={len(results)}.txt"
                write_results_to_file(output_filename, results)

    end_time = time.time()
    logger.info(f"程序运行时间: {end_time - start_time} 秒")
    logger.info(f"结果已写入到 {output_filename}")


if __name__ == "__main__":
    n = int(input("请输入n: "))
    main(n)
