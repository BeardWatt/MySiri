"""
把mp3转换成pcm
"""
from ffmpy3 import FFmpeg
from os import getcwd
from os.path import join


class MP32PCM:
    def __init__(self, i: str, o: str):
        i = join(getcwd(), i)
        o = join(getcwd(), o)
        self.i = i
        self.o = o

    def run(self):
        ff = FFmpeg(
            inputs={self.i: None},
            outputs={self.o: ['-y', '-acodec', 'pcm_s16le', '-f', 's16le', '-ac', '1', '-ar', '16000']}
        )
        ff.run()


if __name__ == '__main__':
    convert = MP32PCM(i='../voice_cache/今天天气怎么样.mp3',
                      o='../voice_cache/今天天气怎么样.pcm')
    convert.run()
