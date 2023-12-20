import sys
import time
from functools import lru_cache
import gmpy2
import numpy as np
from loguru import logger


class Calculate:
    @lru_cache(maxsize=100)
    def matrix_multiply(self, matrix1, matrix2):
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

    @lru_cache(maxsize=100)
    def matrix_power(self, matrix, power):
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
            half_power = self.matrix_power(matrix, power // 2)
            half_power_squared = self.matrix_multiply(half_power, half_power)
            return self.matrix_multiply(matrix, half_power_squared) if power % 2 else half_power_squared

    @lru_cache(maxsize=100)
    def fibonacci(self, n):
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
            powered_matrix = self.matrix_power(matrix, n - 1)
            return powered_matrix[0]

    @lru_cache(maxsize=100)
    def calculate_batch(self, start_index, batch_size):
        """计算一批2-adic数，batch_size 作为参数传递"""
        batch_count = (start_index // batch_size) + 1
        try:
            results = np.zeros(batch_size, dtype=np.int64)  # 使用numpy数组存储结果
            logger.debug(f"开始计算第{batch_count}批2-adic数")
            start_time = time.time()
            for i in range(batch_size):
                index = start_index + i
                fib1 = self.fibonacci(12 * index + 3)
                fib2 = self.fibonacci(12 * index + 4)
                const = gmpy2.mpz(4 * (12 * index + 3) - 1)
                Ln = (const * fib1 + 2 * (12 * index + 3) * fib2) // 5
                result = gmpy2.bit_scan1(Ln)  # 使用gmpy2的bit_scan1来优化循环
                results[i] = result if result is not None else 0
            end_time = time.time()
            logger.success(f"已计算完第{batch_count}批2-adic数, "
                           f"用时{end_time - start_time:.2f}s")
            return results.tolist()  # 将numpy数组转换回列表
        except KeyboardInterrupt:
            sys.exit(1)
        except Exception as e:
            logger.error(f"计算第{batch_count}批2-adic数时发生异常: {e}")
            return []
