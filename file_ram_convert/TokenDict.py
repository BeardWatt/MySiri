"""
从npy文件中读取dict，并写入文件
"""

import numpy as np


class TokenDict:
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
        "APPID": '5f8ffba0',
        "APISecret": 'fb006ab543ed2b029920e07f21f5ce7e',
        "APIKey": '38b3abe70c5866bfe6fb7c4ab36c821d'
    }
    token_dict = TokenDict('../status_saved/aiui.npy', aiui_dict)
    token_dict.save()
