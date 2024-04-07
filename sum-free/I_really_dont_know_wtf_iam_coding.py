def gen_rudin_shapiro_seq(n):
    a = [0] * n
    b = [0] * n
    a[:3] = [0, 1, 1]
    i = 0
    j = 0
    while j <= i <= 500:
        if a[j] == 1:
            if i + 3 <= n:
                b[i:i + 3] = [0, 1, 0]
                i += 3
        if a[j] == 0:
            if i + 3 <= n:
                b[i:i + 3] = [0, 0, 1]
                i += 3
        a[j:i] = b[j:i]
        j += 1
    return b[:i]


def can_add_to_c(temp, sum_free_seq):
    # 简单的检查，确保新添加的数字不是已有两个数字的和
    for i in sum_free_seq:
        for j in sum_free_seq:
            if i + j == temp:
                return False
    return True


def main():
    n = 1000  # 假设n的值为1000
    temp_seq = gen_rudin_shapiro_seq(n)

    # 生成sum-free序列
    sum_free_seq = []
    i = 0
    temp = 1
    while len(sum_free_seq) < n:
        if can_add_to_c(temp, sum_free_seq):
            if temp_seq[i % len(temp_seq)] == 1:
                sum_free_seq.append(temp)
            i += 1
        temp += 1

    print(f"对应的sum-free序列: {sum_free_seq}")
    diff_seq = [sum_free_seq[i + 1] - sum_free_seq[i] for i in range(len(sum_free_seq) - 1)]
    print(f"sum-free序列的差分序列: {diff_seq}")

    filename = f'output_temp_seq_n={n}.txt'
    with open(filename, 'w') as file:
        file.write(f"对应的sum-free序列 (长度 = {len(sum_free_seq)}):\n{sum_free_seq}\n\n")
        file.write(f"sum-free序列的差分序列 (长度 = {len(diff_seq)}):\n{diff_seq}\n")
    print(f"序列已写入到文件 {filename}")


if __name__ == "__main__":
    main()
