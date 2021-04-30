"""
txt转语音ui
"""
import sys
from os.path import getsize, split, splitext
from threading import Thread

import librosa
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSplitter, QVBoxLayout, QPushButton, QTextBrowser, \
    QFileDialog

sys.path.append('../..')
from package.voice_function import V2W as V2W
from package.voice_function.MP32PCM import MP32PCM as MP32PCM


class V2TXT(QWidget):
    manual = "仅支持mp3文件，且音频长度最长50s、仅支持中文普通话"
    file_path = ""

    def __init__(self, parent=None):
        super(V2TXT, self).__init__(parent=parent)
        v_layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Vertical)
        self.current_file_path_monitor = QTextBrowser()
        self.current_file_path_monitor.setFontPointSize(18)
        self.current_file_path_monitor.setMaximumHeight(50)
        self.current_file_path_monitor.setText('当前文件路径：' + self.file_path)
        # 运行状态监视器
        self.runtime_state_monitor = QTextBrowser()
        self.runtime_state_monitor.setFontPointSize(18)
        self.runtime_state_monitor.setText("<h1>" + "语音转txt" + "</h1>")
        self.runtime_state_monitor.append(self.manual)
        # 按钮区
        btn_widget = QWidget()
        btn_widget.setMinimumHeight(150)
        h_layout = QHBoxLayout(self)
        # 选择文件按钮
        self.add_mp3_btn = QPushButton('选择mp3')
        self.add_mp3_btn.clicked.connect(self.get_file_path)
        # 转换按钮
        self.convert_btn = QPushButton('转换')
        self.convert_btn.clicked.connect(self.get_text)
        self.convert_btn.setEnabled(False)

        h_layout.addWidget(self.add_mp3_btn)
        h_layout.addStretch(1)
        h_layout.addWidget(self.convert_btn)
        btn_widget.setLayout(h_layout)
        splitter.addWidget(self.current_file_path_monitor)
        splitter.addWidget(self.runtime_state_monitor)
        splitter.addWidget(btn_widget)
        v_layout.addWidget(splitter)
        self.setLayout(v_layout)

    def get_file_path(self):
        file, file_type = QFileDialog.getOpenFileName(self, "mp3文件选择", "/", "Audio File (*.mp3)")
        # print(file, file_type)
        if file:
            # 判断mp3时长
            duration = librosa.get_duration(filename=file)
            if duration <= 50:
                self.file_path = file
                self.runtime_state_monitor.append('当前选择的文件为：' + split(self.file_path)[-1])
                self.current_file_path_monitor.setText('当前文件路径：' + self.file_path)
                self.runtime_state_monitor.append('mp3长度：' + str(duration) + 's')
                self.convert_btn.setEnabled(True)
            else:
                self.runtime_state_monitor.append('音频持续时间' + str(duration) + 's太长，音频长度最长50s')
        else:
            self.runtime_state_monitor.append('取消选择')

    def get_text(self):
        self.convert_btn.setEnabled(False)
        self.add_mp3_btn.setEnabled(False)

        def converter():
            self.runtime_state_monitor.append(self.file_path + '开始转换')
            pcm_path = splitext(self.file_path)[0] + '.pcm'
            # 先转成pcm文件
            mp3_2_pcm = MP32PCM(i=self.file_path,
                                o=pcm_path)
            mp3_2_pcm.run()
            txt_path = splitext(self.file_path)[0] + '.txt'
            get_words = V2W.get_words(pcm_path=pcm_path)
            with open(txt_path, 'w') as f:
                f.write(get_words)
            self.file_path = ""
            self.add_mp3_btn.setEnabled(True)
            self.runtime_state_monitor.append('识别到：' + get_words)
            self.runtime_state_monitor.append('转换完成，保存为：' + txt_path)

        thread = Thread(target=converter)
        thread.start()
        self.current_file_path_monitor.setText('当前文件路径：')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    custom_font = QFont()
    custom_font.setPointSize(18)
    app.setFont(custom_font)
    widget = V2TXT()
    widget.setGeometry(400, 200, 800, 600)
    widget.show()
    sys.exit(app.exec())
