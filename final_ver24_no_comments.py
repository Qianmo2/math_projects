import time
import logging
import gmpy2
import os
import sys
import re
from functools import lru_cache
from multiprocessing import Pool

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()


@lru_cache(maxsize=4)
def matrix_multiply(matrix1, matrix2):
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
    if n <= 0:
        return gmpy2.mpz(0)
    else:
        matrix = (gmpy2.mpz(1), gmpy2.mpz(1), gmpy2.mpz(0))
        powered_matrix = matrix_power(matrix, n - 1)
        return powered_matrix[0]


@lru_cache(maxsize=4)
def calculate_2adic(index):
    fib1 = fibonacci(12 * index + 3)
    fib2 = fibonacci(12 * index + 4)
    const = gmpy2.mpz(4 * (12 * index + 3) - 1)
    Ln = (const * fib1 + 2 * (12 * index + 3) * fib2) // 5
    times = 0
    while Ln & 1 == 0 and Ln != 0:
        Ln >>= 1
        times += 1
    result = times
    logger.info(f"第 {index + 1} 个数的 2-adic 为：{result}")
    return result


def calculate_batch(start_index):
    batch_size = 100
    results = []
    for i in range(start_index, start_index + batch_size):
        result = calculate_2adic(i)
        results.append(result)
    return results


def read_existing_results(file_path):
    with open(file_path, "r") as f:
        return list(map(int, f.read().strip().split()))


def write_results_to_file(file_path, results):
    with open(file_path, "w", buffering=1024 * 1024) as f:
        f.write(" ".join(map(str, results)))


def get_latest_file_path():
    files = [f for f in os.listdir(".") if re.match(r"output_n=\d+\.txt", f)]
    if not files:
        return None
    return max(files, key=lambda x: int(re.search(r"output_n=(\d+).txt", x).group(1)))


def calculate_results(pool, start_index, end_index, batch_size=100):
    tasks = (end_index - start_index) // batch_size
    result_objects = [pool.apply_async(calculate_batch, args=(i, batch_size)) for i in
                      range(start_index, end_index, batch_size)]
    if (end_index - start_index) % batch_size != 0:
        result_objects.append(pool.apply_async(calculate_batch, args=(
            start_index + tasks * batch_size, (end_index - start_index) % batch_size)))
    return result_objects


def perform_computations(pool, start_index, end_index, batch_size=100):
    tasks = range(start_index, end_index, batch_size)
    result_objects = pool.imap_unordered(calculate_batch, tasks)
    results = []
    try:
        for result in result_objects:
            results.extend(result)
    except KeyboardInterrupt:
        logger.info("用户中断了计算。正在保存当前结果...")
        pool.terminate()
    else:
        pool.close()
    finally:
        pool.join()
        return results, True if isinstance(sys.exc_info()[1], KeyboardInterrupt) else False


def collect_results(result_objects):
    results = []
    for obj in result_objects:
        if obj.ready():
            results.extend(obj.get())
    return results


def initialize_results(latest_file_path):
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


def initialize_pool():
    pool_size = os.cpu_count()
    return Pool(processes=pool_size)


def shutdown_pool(pool, interrupted):
    if interrupted:
        pool.terminate()
    pool.join()


def main_flow(n, latest_file_path):
    results = initialize_results(latest_file_path)
    start_index = len(results)
    if n <= start_index:
        logger.info(f"文件中已包含 {start_index} 个数，无需进行更多计算。")
        return results, f"output_n={n}.txt", True
    pool = initialize_pool()
    new_results, interrupted = perform_computations(pool, start_index, n)
    results.extend(new_results)
    output_filename = f"output_n={len(results)}.txt"
    shutdown_pool(pool, interrupted)
    return results, output_filename, interrupted


def main(n):
    start_time = time.time()
    latest_file_path = get_latest_file_path()
    results, output_filename, interrupted = main_flow(n, latest_file_path)
    write_results_to_file(output_filename, results)
    logger.info(f"结果已写入到 {output_filename}")
    end_time = time.time()
    logger.info(f"程序运行时间: {end_time - start_time} 秒")
    if interrupted:
        return


if __name__ == "__main__":
    try:
        n = int(input("请输入n: "))
        main(n)
    except KeyboardInterrupt:
        logger.info("用户中断了程序。")
