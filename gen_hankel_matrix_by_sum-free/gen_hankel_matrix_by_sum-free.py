import numpy as np


def gen_hankel_needed_seq(max_value):
    a = [0, 1]
    b = [0, 1]
    i = 1
    j = 1

    while j <= i <= max_value:
        if a[j] % 2 == 1:
            i += 1
            # 确保列表足够长
            if i >= len(b):
                b.append(a[j] + 1)
            else:
                b[i] = a[j] + 1
        if a[j] % 2 == 0:
            i += 1
            # 确保列表足够长
            if i >= len(b):
                b.append(a[j])
            else:
                b[i] = a[j]
            i += 1
            # 确保列表足够长
            if i >= len(b):
                b.append(a[j] + 1)
            else:
                b[i] = a[j] + 1
        # 扩展 a 列表以匹配 b 的长度
        if i >= len(a):
            a.extend([0] * (i - len(a) + 1))
        for k in range(j, i + 1):
            a[k] = b[k]
        j += 1

    return b


def create_hankel_matrices(b, max_value):
    hankel_matrices = []
    # 计算可以安全访问的最大矩阵阶数
    max_order_safe = (len(b) - 1) // 2
    for n in range(2, min(max_value, max_order_safe) + 1):
        hankel_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                # 确保索引在范围内
                if i + j < len(b):
                    hankel_matrix[i, j] = b[i + j]
        hankel_matrices.append(hankel_matrix)
    return hankel_matrices


def save_hankel_matrices(hankel_matrices, max_value):
    filename = f'output_hankel_matrices_n={max_value}.txt'
    with open(filename, 'w', encoding='utf-8') as file:
        for index, hankel_matrix in enumerate(hankel_matrices, start=2):
            file.write(f'阶数为 {index} 的汉克尔矩阵:\n[')
            for i, row in enumerate(hankel_matrix):
                row_string = ", ".join([str(int(num)) for num in row])
                if i < len(hankel_matrix) - 1:
                    file.write(f"[{row_string}],\n ")
                else:
                    file.write(f"[{row_string}]")
            file.write("]\n\n")


def main():
    max_value = int(input("请输入一个整数："))
    b = gen_hankel_needed_seq(max_value)
    hankel_matrices = create_hankel_matrices(b, max_value)
    save_hankel_matrices(hankel_matrices, max_value)


if __name__ == "__main__":
    main()
