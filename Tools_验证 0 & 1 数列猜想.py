import os
import re


def get_latest_file():
    # 获取当前目录下所有output_n={n}.txt文件，并找到n最大的文件
    files = [f for f in os.listdir(".") if re.match(r"output_n=\d+\.txt", f)]
    if not files:
        return None
    files.sort(
        key=lambda x: int(re.search(r"output_n=(\d+).txt", x).group(1)), reverse=True
    )
    return files[0]


def process_numbers(numbers):
    current_num = 3  # 从数字3开始
    indexes = []

    while len(numbers) > 1:  # 当列表中不止一个数字时
        try:
            index = numbers.index(current_num)  # 找到当前数字的索引
            indexes.append(index)
            numbers = [num for num in numbers if num != current_num]  # 移除所有当前数字
            current_num += 1  # 移动到下一个数字
        except ValueError:
            break  # 如果当前数字不在列表中，结束循环

    # 如果列表中只剩一个数字，输出它的索引（0或1）
    if len(numbers) == 1:
        indexes.append(0 if numbers[0] == current_num else 1)

    return indexes


def main():
    latest_file = get_latest_file()
    if latest_file:
        print(f"找到最新的文件：{latest_file}")

        with open(latest_file, "r") as file:
            numbers = list(map(int, file.read().strip().split()))  # 读取数字并转换为整数列表

        indexes = process_numbers(numbers)
        print(" ".join(map(str, indexes)))  # 输出结果
    else:
        print("未找到output_n={n}.txt文件。")


if __name__ == "__main__":
    main()
