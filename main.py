import asyncio
from utils.config_loader import config_loader
from loguru import logger

from utils.task_distributor import TaskDistributor


async def main():
    max_threads, latest_number, result_path = config_loader()

    logger.debug(f"最大进程数为 {max_threads}, 最后保存的结果为 {latest_number}, 即将开始计算")
    distributor = TaskDistributor(max_threads=max_threads, latest_number=latest_number, result_file_path=result_path)

    # 开始分配和计算任务
    distributor.distribute_tasks()


if __name__ == "__main__":
    asyncio.run(main())
