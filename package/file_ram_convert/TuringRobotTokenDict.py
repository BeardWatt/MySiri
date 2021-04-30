"""
从npy文件中读取dict，并写入文件
"""

import numpy as np


class TuringRobotTokenDict:
    def __init__(self, file_path: str, token: dict = None):
        self.file_path = file_path
        self.token = token

    # Save
    def save(self):
        np.save(self.file_path, self.token)

    # Load
    def load(self) -> dict:
        return np.load(self.file_path, allow_pickle=True).item()


if __name__ == "__main__":
    aiui_dict = {
        "APIKey": 'fafa0debb9ca422096ccbcd8d1f92863'
    }
    token_dict = TuringRobotTokenDict('../status_saved/turingRobot.npy', aiui_dict)
    token_dict.save()
    print(token_dict.load())
