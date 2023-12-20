import json
import os


class ConfigLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.config_data = {}

    def load_config(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"配置文件 {self.filepath} 未找到。")

        with open(self.filepath, 'r') as file:
            self.config_data = json.load(file)

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def update_max_threads(self, max_threads: int) -> bool:
        if not isinstance(max_threads, int):
            raise ValueError("max_threads 必须是一个整数")
        self.config_data['max_threads'] = max_threads
        try:
            self.save_config()
            return True
        except Exception as e:
            raise e

    def save_config(self):
        with open(self.filepath, 'w') as file:
            json.dump(self.config_data, file, indent=4)
