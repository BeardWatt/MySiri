"""
主窗口ui

包含：
1、主窗口一分为二，水平布局：
    左侧功能区，右侧说明区
2、菜单栏：

"""
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QSplitter

from FunctionWidget import FunctionWidget
from ManualWidget import ManualWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setGeometry(200, 100, 1500, 900)
        # 分割线
        splitter = QSplitter(Qt.Horizontal)

        function_widget = FunctionWidget()
        self.status = self.statusBar()
        function_widget.begin_save_signal.connect(self.handle_begin_save)
        function_widget.saved_signal.connect(self.handle_saved)
        manual_widget = ManualWidget()
        # 设置最小宽度
        manual_widget.setMinimumWidth(300)

        # 添加组件
        splitter.addWidget(function_widget)
        splitter.addWidget(manual_widget)
        # 设置初始比例，
        splitter.setStretchFactor(index=0, stretch=7)
        splitter.setStretchFactor(index=1, stretch=3)

        self.setCentralWidget(splitter)

    # ***：开始保存
    def handle_begin_save(self, s: str, duration: int):
        self.status.showMessage(s, duration)

    # ***：已保存
    def handle_saved(self, s: str, duration: int):
        self.status.showMessage(s, duration)


def run():
    application = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('../img/app.ico'))
    # custom_font = QFont()
    # custom_font.setPointSize(15)
    # app.setFont(custom_font)
    mainWindow = MainWindow()
    mainWindow.setWindowIcon(QIcon('../img/app.ico'))
    mainWindow.show()
    sys.exit(app.exec())
