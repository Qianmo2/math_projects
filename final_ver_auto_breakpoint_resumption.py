import time
import logging
import gmpy2
import os
import re
from multiprocessing import Pool

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()


def matrix_multiply(matrix1, matrix2):
    a, b, c = matrix1
    d, e, f = matrix2
    return (
        gmpy2.mul(a, d) + gmpy2.mul(b, e),
        gmpy2.mul(a, e) + gmpy2.mul(b, f),
        gmpy2.mul(b, e) + gmpy2.mul(c, f),
    )


def matrix_power(matrix, power):
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
    if n <= 0:
        return gmpy2.mpz(0)
    else:
        matrix = (gmpy2.mpz(1), gmpy2.mpz(1), gmpy2.mpz(0))
        powered_matrix = matrix_power(matrix, n - 1)
        return powered_matrix[0]


def how_times_Ln_divided_2(ln):
    times = 0
    bit_length = ln.bit_length()
    while bit_length > 0:
        if ln.is_even():
            ln = gmpy2.f_div_2exp(ln, 1)
            times += 1
        else:
            break
        bit_length -= 1
    return times


def get_latest_file():
    files = [f for f in os.listdir(".") if re.match(r"output_n=\d+\.txt", f)]
    if not files:
        return None
    files.sort(
        key=lambda x: int(re.search(r"output_n=(\d+).txt", x).group(1)), reverse=True
    )
    return files[0]


def calculate_2adic(index):
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

    if n <= start_index:
        logger.info(f"文件中已包含 {start_index} 个数，无需进行更多计算。")
        output_filename = f"output_n={n}.txt"
        with open(output_filename, "w") as f:
            f.write(" ".join(map(str, results[:n])))
    else:
        with Pool() as p:
            new_results = p.map(calculate_2adic, range(start_index, n))
            results.extend(new_results)

        output_filename = f"output_n={n}.txt"
        with open(output_filename, "w") as f:
            f.write(" ".join(map(str, results)))

    end_time = time.time()
    logger.info(f"程序运行时间: {end_time - start_time} 秒")
    logger.info(f"结果已写入到 {output_filename}")


if __name__ == "__main__":
    n = int(input("请输入n: "))
    main(n)
