"""
录制一条音频
"""
import pyaudio
import wave
from MP32PCM import MP32PCM


class Recorder:
    CHUNK = 16  # 每个缓冲区的帧数
    FORMAT = pyaudio.paInt16  # 采样位数
    CHANNELS = 1  # 单声道
    RATE = 16000  # 采样频率

    def __init__(self):
        self.p = pyaudio.PyAudio()

    def record(self):
        stream = self.p.open(format=self.FORMAT,
                             channels=self.CHANNELS,
                             rate=self.RATE,
                             input=True,
                             frames_per_buffer=self.CHUNK)  # 打开流，传入响应参数
        wf = wave.open(r'../voice_cache/v2w.mp3', 'wb')  # 打开 mp3 文件。
        wf.setnchannels(self.CHANNELS)  # 声道设置
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))  # 采样位数设置
        wf.setframerate(self.RATE)  # 采样频率设置
        for _ in range(0, int(self.RATE * 10 / self.CHUNK)):
            data = stream.read(self.CHUNK)
            wf.writeframes(data)  # 写入数据
        stream.stop_stream()  # 关闭流
        stream.close()
        self.p.terminate()
        wf.close()

        convert = MP32PCM(i='../voice_cache/v2w.mp3',
                          o='../voice_cache/v2w.pcm')
        convert.run()


if __name__ == '__main__':
    recorder = Recorder()
    recorder.record()
