import os
import re
import time

from config.config import ConfigLoader
from loguru import logger


def config_loader():
    """配置文件读取"""
    logger.info("开始读取配置文件...")
    config_manager = ConfigLoader("config/config.json")
    config_manager.load_config()

    max_threads = config_manager.get("max_threads")
    result_path = config_manager.get("result_file_path")

    # 获取保存的结果文件
    files = [f for f in os.listdir(result_path) if re.match(r"output_n=\d+\.txt", f)]
    if not files:
        logger.info("未能找到保存的结果文件, 从0开始计算")
        latest_number = 0
    else:
        latest_file = max(files, key=lambda x: int(re.search(r"output_n=(\d+).txt", x).group(1)))
        latest_number = int(re.search(r"output_n=(\d+).txt", latest_file).group(1))
        logger.info(f"已从文件 {latest_file} 中读取 最后保存的结果为 {latest_number}")

    # 获取cpu核心数
    cpu_cores = os.cpu_count()
    if cpu_cores / 2 > max_threads:
        logger.error(f"当前物理机CPU核心数为{cpu_cores}, 推荐使用的最大线程数为{max_threads / 2}, 分配不合理")

        try:
            time.sleep(1)  # 等待异步log输出完毕
            _ = int(input(f"请输入相关设置:\n1. CPU核心数的一半 {max_threads / 2}\n"
                          f"2.塞满CPU {cpu_cores}\n或者输入你想要的进程数(默认选1): "))
        except Exception as e:
            logger.error(f"输入不合法, 自动选择选项1: {e}")
            _ = 1

        # 判断输入是否合法
        if not isinstance(_, int):
            logger.error("输入不合法, 自动选择选项1")
            _ = 1

        if _ == 1:
            max_threads = cpu_cores / 2
        elif _ == 2:
            max_threads = cpu_cores
        elif _ < 0 or _ > cpu_cores:
            logger.error("输入不合法, 自动选择选项1")
            max_threads = cpu_cores / 2
        else:
            max_threads = _

        max_threads = int(max_threads)
        logger.info(f"最大线程数为 {max_threads}")
        try:
            config_manager.update_max_threads(max_threads=max_threads)
            logger.debug("更新配置文件成功")
        except Exception as e:
            logger.error(f"更新配置文件失败: {e}")

    elif max_threads > cpu_cores:
        logger.warning(f"当前物理机CPU核心数为{cpu_cores}, 配置文件中的最大线程数为{max_threads}, 超出物理机核心数")
        logger.debug(f"将自动将最大线程数设置为物理机核心数的一半")
        try:
            config_manager.update_max_threads(max_threads=cpu_cores / 2)
            max_threads = cpu_cores / 2
            logger.debug("更新配置文件成功")
        except Exception as e:
            logger.error(f"更新配置文件失败: {e}")

    logger.success("配置文件读取完毕")
    return max_threads, latest_number, result_path
