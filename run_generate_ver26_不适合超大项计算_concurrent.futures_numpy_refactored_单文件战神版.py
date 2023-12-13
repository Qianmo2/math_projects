import time
import logging
import gmpy2
import os
import sys
import re
import numpy as np
from functools import lru_cache
from functools import partial
from concurrent.futures import ProcessPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()


@lru_cache(maxsize=4)
def matrix_multiply(matrix1, matrix2):
    """
    矩阵乘法

    一个三元组(a, b, c)被用来表示一个2x2的矩阵
    | a b | * | d e |
    | b c |   | e f |
    """

    a, b, c = matrix1
    d, e, f = matrix2
    be = gmpy2.mul(b, e)
    return (
        gmpy2.mul(a, d) + be,
        gmpy2.mul(a, e) + gmpy2.mul(b, f),
        be + gmpy2.mul(c, f),
    )


@lru_cache(maxsize=4)
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


@lru_cache(maxsize=4)
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


@lru_cache(maxsize=4)
def calculate_batch(start_index, batch_size):
    """计算一批2-adic数，batch_size 作为参数传递"""
    results = np.zeros(batch_size, dtype=np.int64)  # 使用numpy数组存储结果
    for i in range(batch_size):
        index = start_index + i
        fib1 = fibonacci(12 * index + 3)
        fib2 = fibonacci(12 * index + 4)
        const = gmpy2.mpz(4 * (12 * index + 3) - 1)
        Ln = (const * fib1 + 2 * (12 * index + 3) * fib2) // 5
        result = gmpy2.bit_scan1(Ln)  # 使用gmpy2的bit_scan1来优化循环
        results[i] = result if result is not None else 0
        logger.info(f"第 {index + 1} 个数的 2-adic 为：{results[i]}")
    return results.tolist()  # 将numpy数组转换回列表


def read_existing_results(file_path):
    """读取已有结果"""
    with open(file_path, "r") as f:
        return list(map(int, f.read().strip().split()))


def write_results_to_file(file_path, results):
    """写入结果到文件"""
    with open(file_path, "w", buffering=1024 * 1024) as f:  # 使用1MB的缓冲区
        f.write(" ".join(map(str, results)))


def get_latest_file_path():
    """获取最新文件路径"""
    files = [f for f in os.listdir(".") if re.match(r"output_n=\d+\.txt", f)]
    if not files:
        return None
    return max(files, key=lambda x: int(re.search(r"output_n=(\d+).txt", x).group(1)))


def perform_computations(start_index, end_index, batch_size=100):
    """启动计算并使用 as_completed 获取结果"""
    tasks = range(start_index, end_index, batch_size)
    calculate_batch_with_size = partial(calculate_batch, batch_size=batch_size)

    results = []
    interrupted = False
    with ProcessPoolExecutor() as executor:
        future_to_index = {executor.submit(calculate_batch_with_size, task): task for task in tasks}

        try:
            for future in as_completed(future_to_index):
                result = future.result()
                results.extend(result)
        except KeyboardInterrupt:
            logger.info("用户中断了计算。正在保存当前结果...")
            interrupted = True
            # 取消所有正在运行或等待的任务
            for future in future_to_index:
                future.cancel()
        except Exception as e:
            logger.error(f"计算过程中发生错误: {e}")
            interrupted = True
            # 取消所有正在运行或等待的任务
            for future in future_to_index:
                future.cancel()

    return results, interrupted


def initialize_results(latest_file_path):
    """初始化结果列表"""
    if latest_file_path:
        try:
            results = read_existing_results(latest_file_path)
            logger.info(f"已从文件 {latest_file_path} 中读取 {len(results)} 个结果。")
            return results
        except FileNotFoundError:
            logger.info("文件不存在，将创建新文件并从头开始计算。")
    else:
        logger.info("未找到现有文件，将创建新文件并从头开始计算。")
    return []


def main_flow(n, latest_file_path, batch_size=100):
    """流程控制函数"""
    results = initialize_results(latest_file_path)
    start_index = len(results)
    if n <= start_index:
        logger.info(f"文件中已包含 {start_index} 个数，无需进行更多计算。")
        return results, f"output_n={n}.txt", True

    new_results, interrupted = perform_computations(start_index, n, batch_size)
    results.extend(new_results)
    output_filename = f"output_n={len(results)}.txt"
    return results, output_filename, interrupted


def main(n):
    """主函数"""
    start_time = time.time()
    latest_file_path = get_latest_file_path()
    results, output_filename, interrupted = main_flow(n, latest_file_path)
    write_results_to_file(output_filename, results)
    logger.info(f"结果已写入到 {output_filename}")
    end_time = time.time()
    logger.info(f"程序运行时间: {end_time - start_time} 秒。")


if __name__ == "__main__":
    try:
        n = int(input("请输入n: "))
        main(n)
    except KeyboardInterrupt:
        logger.info("用户中断了程序。")
