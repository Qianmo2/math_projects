import time
import logging
import gmpy2
from joblib import Parallel, delayed


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
        if power % 2 == 0:
            return matrix_multiply(half_power, half_power)
        else:
            return matrix_multiply(matrix, matrix_multiply(half_power, half_power))


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


def calculate_2adic(index):
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger()
    fib1 = fibonacci(12 * index + 3)
    fib2 = fibonacci(12 * index + 4)
    const = gmpy2.mpz(4 * (12 * index + 3) - 1)
    Ln = (const * fib1 + 2 * (12 * index + 3) * fib2) // 5
    result = how_times_Ln_divided_2(Ln)
    logger.info(f"第 {index + 1} 个数的 2-adic 为：{result}")
    return result


def main(n):
    start_time = time.time()

    results = Parallel(n_jobs=-1)(delayed(calculate_2adic)(i) for i in range(n))

    with open("output_all_num", "w") as f:
        f.write(" ".join(map(str, results)))

    end_time = time.time()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger = logging.getLogger()
    logger.info(f"程序运行时间: {end_time - start_time} 秒")


if __name__ == "__main__":
    n = int(input("请输入n: "))
    main(n)
