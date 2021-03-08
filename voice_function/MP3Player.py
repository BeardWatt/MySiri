"""
播放mp3
"""
from playsound import playsound


class MP3Player:
    def __init__(self, mp3_path):
        self.mp3_path = mp3_path

    def player(self):
        playsound(self.mp3_path)


if __name__ == '__main__':
    mp3_player = MP3Player(r'../voice_cache/w2v.mp3')
    mp3_player.player()
