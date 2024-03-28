import os
import re
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger()


def get_latest_file():
    # 获取当前目录下所有output_n={n}.txt文件，并找到n最大的文件
    files = [f for f in os.listdir(".") if re.match(r"output_n=\d+\.txt", f)]
    if not files:
        return None
    files.sort(
        key=lambda x: int(re.search(r"output_n=(\d+).txt", x).group(1)), reverse=True
    )
    return files[0]


def find_unique_num_position(matrix, x):
    """
    小心列表索引超出范围！！！
    需要确保在创建 results_matrix 时，每行都有完整的x个元素
    或者在 find_unique_num_position() 中处理不完整行的情况
    还需要确保至少有两行数据来比较，这样才能找到唯一的数字位置。
    """
    # 确保矩阵至少有两行数据
    if len(matrix) < 2:
        return None
    # 对于每一列，检查前两行是否所有元素都相同，如果不是，则该列包含unique_num
    for col_index in range(min(x, len(matrix[0]))):  # 确保不会超出列的范围
        if matrix[0][col_index] != matrix[1][col_index]:
            return col_index
    return None


def main():
    latest_file = get_latest_file()
    if latest_file:
        n_value = re.search(r"output_n=(\d+).txt", latest_file).group(1)
        output_filename = f"output_Tools_自动查找每个数字出现在数列的第几项_n={n_value}.txt"
        logger.info(f"找到最新的文件：{latest_file}")

        with open(latest_file, "r") as file:
            numbers = list(map(int, file.read().strip().split()))

        # 预定义的每行包含项数x的列表，x为2的幂
        x_values = [2**i for i in range(1, int(len(numbers) ** 0.5) + 1)]

        start_time = time.time()

        with open(output_filename, "w") as output_file:
            for x in x_values:
                if x > len(numbers):  # 如果x值超过了列表长度，就没有必要继续计算
                    output_file.write(
                        f"总项数 = {n_value:<10}每行包含项数 = {x:<10}unique_num = 未找到\n"
                    )
                    logger.info(f"每行包含项数 = {x} 时，超过了总项数，停止计算。")
                    break  # 终止循环

                # 将数列按照每行x个数分行
                results_matrix = [numbers[i : i + x] for i in range(0, len(numbers), x)]
                # 计算unique_num的位置
                unique_index = find_unique_num_position(results_matrix, x)
                """
                {n_value:<10} {x:<10} {unique_index + 1:<10}
                这些占位符的 <10 表示该字段将被格式化为最小宽度为10的左对齐文本
                """
                if unique_index is not None:
                    output_file.write(
                        "总项数 = {0:<10}每行包含项数 = {1:<10}unique_num = 第 {2:<10} 位\n".format(
                            n_value, x, unique_index + 1
                        )
                    )
                else:
                    output_file.write(
                        "总项数 = {0:<10}每行包含项数 = {1:<10}unique_num = 未找到\n".format(
                            n_value, x
                        )
                    )

        end_time = time.time()
        logger.info(f"程序运行时间: {end_time - start_time} 秒")

    else:
        logger.info("未找到output_n={n}.txt文件。")


if __name__ == "__main__":
    main()
