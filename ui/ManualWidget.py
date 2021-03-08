"""
说明区ui

"""
import sys
from os import getcwd
from PyQt5.QtWidgets import QApplication, QWidget, QSplitter, QVBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont


class ManualWidget(QWidget):
    manual_path = r'../status_saved/manual.html'
    words_path = r'../status_saved/words.html'

    def __init__(self, parent=None):
        super(ManualWidget, self).__init__(parent=parent)
        v_layout = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)
        # 功能说明
        manual = QWebEngineView()
        with open(self.manual_path, 'r') as f:
            manual.setHtml(f.read())
        # 寄语
        words = QWebEngineView()
        with open(self.words_path, 'r') as f:
            words.setHtml(f.read())

        splitter.addWidget(manual)
        splitter.addWidget(words)
        splitter.setStretchFactor(0, 5)
        splitter.setStretchFactor(1, 5)
        v_layout.addWidget(splitter)
        self.setLayout(v_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # custom_font = QFont()
    # custom_font.setPointSize(18)
    # app.setFont(custom_font)
    widget = ManualWidget()
    widget.setGeometry(400, 200, 800, 600)
    widget.show()
    sys.exit(app.exec())
