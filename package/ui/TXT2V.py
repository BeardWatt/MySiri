"""
txt转语音ui
"""
import sys
from os.path import getsize, split, splitext
from threading import Thread

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QSplitter, QVBoxLayout, QPushButton, QTextBrowser, \
    QFileDialog

sys.path.append('../..')
from package.voice_function import W2V as W2V


class TXT2V(QWidget):
    manual = "仅支持txt文件，且文本长度需小于4000字节（约1000汉字）"
    file_path = ""
    file_contain = ""

    def __init__(self, parent=None):
        super(TXT2V, self).__init__(parent=parent)
        v_layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Vertical)
        self.current_file_path_monitor = QTextBrowser()
        self.current_file_path_monitor.setFontPointSize(18)
        self.current_file_path_monitor.setMaximumHeight(50)
        self.current_file_path_monitor.setText('当前文件路径：' + self.file_path)
        # 运行状态监视器
        self.runtime_state_monitor = QTextBrowser()
        self.runtime_state_monitor.setFontPointSize(18)
        self.runtime_state_monitor.setText("<h1>" + "txt转语音" + "</h1>")
        self.runtime_state_monitor.append(self.manual)
        # 按钮区
        btn_widget = QWidget()
        btn_widget.setMinimumHeight(150)
        h_layout = QHBoxLayout(self)
        # 选择文件按钮
        self.add_txt_btn = QPushButton('选择txt')
        self.add_txt_btn.clicked.connect(self.get_file_path)
        # 转换按钮
        self.convert_btn = QPushButton('转换')
        self.convert_btn.clicked.connect(self.get_voice)
        self.convert_btn.setEnabled(False)

        h_layout.addWidget(self.add_txt_btn)
        h_layout.addStretch(1)
        h_layout.addWidget(self.convert_btn)
        btn_widget.setLayout(h_layout)
        splitter.addWidget(self.current_file_path_monitor)
        splitter.addWidget(self.runtime_state_monitor)
        splitter.addWidget(btn_widget)
        v_layout.addWidget(splitter)
        self.setLayout(v_layout)

    def get_file_path(self):
        file, file_type = QFileDialog.getOpenFileName(self, "txt文件选择", "/", "Text File (*.txt)")
        # 是否成功选择了文件
        if file:
            if getsize(file) <= 4000:
                self.file_path = file
                self.runtime_state_monitor.append('当前选择的文件为：' + split(self.file_path)[-1])
                self.current_file_path_monitor.setText('当前文件路径：' + self.file_path)
                with open(self.file_path, 'r') as f:
                    self.file_contain = f.read()
                    self.runtime_state_monitor.append('txt内容：' + self.file_contain)
                self.convert_btn.setEnabled(True)
            else:
                self.runtime_state_monitor.append('文件太大，文本长度需小于4000字节（约1000汉字）')
        else:
            self.runtime_state_monitor.append('取消选择')

    def get_voice(self):
        self.convert_btn.setEnabled(False)
        self.add_txt_btn.setEnabled(False)

        def converter():
            self.runtime_state_monitor.append(self.file_path + '开始转换')
            mp3_path = splitext(self.file_path)[0] + '.mp3'
            gap = W2V.get_voice(self.file_contain, mp3_path)
            self.file_path = ""
            self.file_contain = ""
            self.add_txt_btn.setEnabled(True)
            self.runtime_state_monitor.append('转换完成，保存为：' + mp3_path)

        thread = Thread(target=converter)
        thread.start()
        self.current_file_path_monitor.setText('当前文件路径：')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    custom_font = QFont()
    custom_font.setPointSize(18)
    app.setFont(custom_font)
    widget = TXT2V()
    widget.setGeometry(400, 200, 800, 600)
    widget.show()
    sys.exit(app.exec())
