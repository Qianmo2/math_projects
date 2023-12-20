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


def find_number_positions(filename):
    # 读取文件并找出每个数字出现的位置
    number_positions = {}
    with open(filename, "r") as file:
        numbers = file.read().strip().split()
        for index, number in enumerate(numbers, start=1):  # 从1开始计数
            if number not in number_positions:
                number_positions[number] = []
            number_positions[number].append(index)
    return number_positions


def main():
    latest_file = get_latest_file()
    if latest_file:
        print(f"找到最新的文件：{latest_file}")
        n_value = re.search(r"output_n=(\d+).txt", latest_file).group(1)
        output_filename = f"output_n={n_value}_Tools_自动查找每个数字出现在数列的第几项_.txt"

        number_positions = find_number_positions(latest_file)

        # 对数字进行排序，确保输出按照数字顺序进行
        sorted_numbers = sorted(number_positions.keys(), key=int)

        with open(output_filename, "w", encoding="utf-8") as output_file:
            for number in sorted_numbers:
                positions = number_positions[number]
                line = f"数字 {number} 出现在位置：\n{positions}\n\n"
                print(line, end="")  # 输出到控制台
                output_file.write(line)  # 写入到文件

        print(f"结果已写入到 {output_filename}")
    else:
        print("未找到output_n={n}.txt文件。")


if __name__ == "__main__":
    main()
