# cython_fib.pyx
from cpython cimport bool
from gmpy2 cimport mpz, mul
from libc.stdint cimport int64_t

# 定义一个 C struct 来代替原来用元组表示的矩阵
cdef struct Matrix2x2:
    mpz a
    mpz b
    mpz c

cpdef Matrix2x2 matrix_multiply(Matrix2x2 matrix1, Matrix2x2 matrix2):
    """
    矩阵乘法优化版本，使用了静态类型声明来提高性能。
    """
    cdef mpz ad = mul(matrix1.a, matrix2.a)
    cdef mpz be = mul(matrix1.b, matrix2.b)
    cdef Matrix2x2 result
    result.a = ad + be
    result.b = mul(matrix1.a, matrix2.b) + mul(matrix1.b, matrix2.c)
    result.c = be + mul(matrix1.c, matrix2.c)
    return result
