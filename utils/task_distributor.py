import multiprocessing
import os
import traceback
from loguru import logger
from core.calculate import Calculate


class TaskDistributor:
    def __init__(self, max_threads: int, latest_number: int, result_file_path: str):
        self.calculate = Calculate()
        self.max_threads = max_threads
        self.latest_number = latest_number
        self.result_file_path = result_file_path
        self.pool = multiprocessing.Pool(max_threads)
        self.batch_size = 2000

    def distribute_tasks(self):
        try:
            # 这个字典将跟踪每个进程的开始索引
            start_indices = {i: self.latest_number + i * self.batch_size for i in range(self.max_threads)}
            while True:
                results_futures = []
                for i in range(self.max_threads):
                    start_index = start_indices[i]
                    future = self.pool.apply_async(self.calculate.calculate_batch, (start_index, self.batch_size))
                    results_futures.append((i, future))

                all_results = []
                # 等待当前批次的所有进程完成
                for i, future in results_futures:
                    # 等待结果
                    results = future.get()
                    if results:  # 如果结果不为空
                        all_results.append(results)

                # 保存结果
                self.save_results(all_results, start_indices)

                # 更新索引
                for i in range(self.max_threads):
                    start_indices[i] += self.batch_size * self.max_threads

        except KeyboardInterrupt:
            # 极小的概率会在这里触发
            logger.info("检测到键盘中断，正在关闭所有进程...")
            self.pool.terminate()  # 立即停止所有进程
            self.pool.join()
        except Exception as e:
            logger.warning(f"发生异常: {e}, 将立即停止所有进程")
            traceback.print_exc()  # 打印异常信息
            self.pool.terminate()  # 立即停止所有进程
        finally:
            self.pool.close()  # 关闭进程池
            self.pool.join()  # 等待进程池中的进程结束
            logger.debug("所有进程已结束, 程序即将退出")

    def save_results(self, results, start_indices):
        for i, text in enumerate(results):

            if text:
                file_path = os.path.join(self.result_file_path, f"output_n={start_indices[i]+2000}.txt")
                with open(file_path, "w") as file:
                    file.write(str(text))
            else:
                continue
