# 参与人员
# gen_sum-free_seq 函数原型（C++） & main函数的生成sum-free序列模块原型（C++）：刘文昊
# gen_rudin_shapiro_seq 函数原型（C++）：王长瑞
# 代码优化、整合并支持用户自定义输出长度（Python）：张祚洲

def calculate_power(x, y):
    return x ** (y + 1)




def gen_rudin_shapiro_seq(n):
    # 初始化Rudin-Shapiro序列
    a = ['a']
    i = 0

    # 生成Rudin-Shapiro序列直到达到所需长度n
    while len(a) < n:
        # 计算2的i次幂，用于确定当前迭代中需要处理的元素数量
        next_power = calculate_power(2, i)
        # 如果需要更多元素，则扩展列表a
        if next_power * 2 > len(a):
            a.extend([''] * (next_power * 2 - len(a)))
        # 根据Rudin-Shapiro规则更新序列
        for j in range(next_power):
            if 2 * j + 1 >= n:
                break
            if a[j] == 'a':
                a[2 * j], a[2 * j + 1] = 'a', 'b'
            elif a[j] == 'b':
                a[2 * j], a[2 * j + 1] = 'a', '2'
            elif a[j] == '1':
                a[2 * j], a[2 * j + 1] = '1', '2'
            elif a[j] == '2':
                a[2 * j], a[2 * j + 1] = '1', 'b'
        i += 1

    # 转换Rudin-Shapiro序列中的字符为数字序列
    b = [0 if char in ['a', 'b'] else 1 for char in a if char][:n]

    return b


def can_add_to_c(b, c):
    # 检查数字b是否可以添加到sum-free序列c中
    for num in c:
        if num + b in c or num * 2 == b or num == b:
            return False
    return True


def main():
    # 获取用户输入并生成Rudin-Shapiro序列
    n = int(input("请输入欲生成的 Rudin-Shapiro 序列长度: "))
    rudin_shapiro_seq = gen_rudin_shapiro_seq(n)

    # 生成sum-free序列
    sum_free_seq = []
    i = 0
    temp = 1
    while len(sum_free_seq) < n:
        if can_add_to_c(temp, sum_free_seq):
            if rudin_shapiro_seq[i % len(rudin_shapiro_seq)] == 1:
                sum_free_seq.append(temp)
            i += 1
        temp += 1

    print(f"Rudin-Shapiro序列: {rudin_shapiro_seq}")
    print(f"对应的sum-free序列: {sum_free_seq}")
    diff_seq = [sum_free_seq[i + 1] - sum_free_seq[i] for i in range(len(sum_free_seq) - 1)]
    print(f"sum-free序列的差分序列: {diff_seq}")

    filename = f'output_Rudin-Shapiro_n={n}.txt'
    with open(filename, 'w') as file:
        file.write(f"Rudin-Shapiro序列 (长度 = {n}):\n{rudin_shapiro_seq}\n\n")
        file.write(f"对应的sum-free序列 (长度 = {len(sum_free_seq)}):\n{sum_free_seq}\n\n")
        file.write(f"sum-free序列的差分序列 (长度 = {len(diff_seq)}):\n{diff_seq}\n")
    print(f"序列已写入到文件 {filename}")


if __name__ == "__main__":
    main()
