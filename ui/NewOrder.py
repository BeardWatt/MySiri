"""
新指令ui
"""
import sys
import wave
from threading import Thread
from time import sleep

import pyaudio
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSplitter, QVBoxLayout, QPushButton, QTextBrowser, \
    QLCDNumber

import voice_function.V2W as V2W
import voice_function.AgeSex as AgeSex
import voice_function.Emotion as Emotion
import voice_function.W2V as W2V
from voice_function.MP32PCM import MP32PCM
from voice_function.MP3Player import MP3Player
from voice_function.TuringRobot import TuringRobot


class NewOrder(QWidget):
    lcd_num = 10
    # 主按钮的状态
    # 0：未启动
    # 1：正在听取指令
    # 2：正在处理指令
    main_btn_status = 0

    def __init__(self, parent=None, title_text: str = ''):
        super(NewOrder, self).__init__(parent=parent)
        self.title_text = title_text
        v_layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Vertical)
        # 运行状态监视器
        self.runtime_state_monitor = QTextBrowser()
        self.runtime_state_monitor.setFontPointSize(18)
        self.runtime_state_monitor.setText("<h1>" + self.title_text + "</h1>")
        # 按钮区
        btn_widget = QWidget()
        btn_widget.setMinimumHeight(150)
        h_layout = QHBoxLayout(self)
        # 主按钮
        self.btn_main = QPushButton("Go")
        self.btn_main.clicked.connect(self.on_clicked_main_btn)
        self.btn_main.clicked.connect(self.handle_countdown)
        # 倒计时，10秒
        self.countdown = QLCDNumber()
        self.countdown.setLineWidth(0)
        self.countdown.setDigitCount(3)
        self.countdown.display(str(self.lcd_num))
        # 计时
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_lcd)

        h_layout.addWidget(self.countdown)
        h_layout.addWidget(self.btn_main, alignment=Qt.AlignLeft)
        btn_widget.setLayout(h_layout)
        splitter.addWidget(self.runtime_state_monitor)
        splitter.addWidget(btn_widget)
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 5)
        v_layout.addWidget(splitter)
        self.setLayout(v_layout)

    # 主按钮点击
    def on_clicked_main_btn(self):
        if self.main_btn_status == 0:
            self.runtime_state_monitor.append("开始新指令")
            self.main_btn_status = 1

            # 开始录音
            def recorder():
                CHUNK = 16  # 每个缓冲区的帧数
                FORMAT = pyaudio.paInt16  # 采样位数
                CHANNELS = 1  # 单声道
                RATE = 16000  # 采样频率
                p = pyaudio.PyAudio()
                stream = p.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True,
                                frames_per_buffer=CHUNK)  # 打开流，传入响应参数
                wf = wave.open(r'../voice_cache/v2w.mp3', 'wb')  # 打开 mp3 文件。
                wf.setnchannels(CHANNELS)  # 声道设置
                wf.setsampwidth(p.get_sample_size(FORMAT))  # 采样位数设置
                wf.setframerate(RATE)  # 采样频率设置
                while self.main_btn_status == 1:
                    data = stream.read(CHUNK)
                    wf.writeframes(data)  # 写入数据
                stream.stop_stream()  # 关闭流
                stream.close()
                p.terminate()
                wf.close()
                convert = MP32PCM(i='../voice_cache/v2w.mp3',
                                  o='../voice_cache/v2w.pcm')
                convert.run()

            thread = Thread(target=recorder)
            thread.start()
        elif self.main_btn_status == 1:
            self.btn_main.setEnabled(False)
            self.main_btn_status = 2
            self.handle_order()

    # 处理指令
    def handle_order(self):
        def handler():
            sleep(1)
            self.runtime_state_monitor.append("正在处理")
            ''''''
            respond_text = 'Biser'
            if self.title_text == '新指令':
                get_words = V2W.get_words()
                self.runtime_state_monitor.append('识别到：' + get_words)
                turing_robot = TuringRobot(get_words)
                respond_text = turing_robot.get_respond()
            elif self.title_text == '年龄、性别识别':
                respond_text = AgeSex.get_age_sex()
            elif self.title_text == '情感分析':
                get_words = V2W.get_words()
                self.runtime_state_monitor.append('识别到：' + get_words)
                respond_text = Emotion.get_emotion(get_words)

            gap = W2V.get_voice(respond_text)
            self.runtime_state_monitor.append(respond_text)
            mp3_player = MP3Player(r'../voice_cache/w2v.mp3')
            mp3_player.player()
            ''''''
            self.main_btn_status = 0
            self.btn_main.setEnabled(True)
            self.runtime_state_monitor.append("处理结束\n")
            self.countdown.display("10")

        thread = Thread(target=handler)
        thread.start()

    # 开始QLCDNumber倒计时
    def handle_countdown(self):
        self.timer.stop()
        self.lcd_num = 10
        if self.main_btn_status == 1:
            self.countdown.display("10")
            self.timer.start(1000)

    # 刷新QLCDNumber
    def refresh_lcd(self):
        if self.lcd_num > 1:
            self.lcd_num -= 1
            self.countdown.display(str(self.lcd_num))
        else:
            self.timer.stop()
            self.btn_main.setEnabled(False)
            self.main_btn_status = 2
            self.lcd_num = 10
            self.countdown.display("0")
            self.handle_order()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    custom_font = QFont()
    custom_font.setPointSize(18)
    app.setFont(custom_font)
    widget = NewOrder()
    widget.setGeometry(400, 200, 800, 600)
    widget.show()
    sys.exit(app.exec())
