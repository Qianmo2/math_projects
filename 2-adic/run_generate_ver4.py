from fractions import Fraction


def fibonacci(n):
    fib = [Fraction(0), Fraction(1)] + [Fraction(0)] * (n - 1)  # 使用分数存储结果
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
    return fib[n]


def how_times_Ln_divided_2(ln):  # 返回Ln可以被2整除多少次
    times = 0
    while ln % 2 == 0:
        ln //= 2
        times += 1
    return times


n = int(input("请输入n: "))

with open("output.txt", "w") as f:
    for i in range(n):
        # 定义Ln数列
        Ln = (
            (4 * (12 * i + 3) - 1) * fibonacci(12 * i + 3)
            + 2 * (12 * i + 3) * fibonacci((12 * i + 3) + 1)
        ) // 5
        result = how_times_Ln_divided_2(Ln)
        print(f"第 {i + 1} 个数的2-adic为：{result}")
        f.write(f"{result} ")
        i += 1
