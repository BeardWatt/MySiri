"""
讯飞Token
"""
import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTreeWidget, QSplitter, QFrame, QTreeWidgetItem, \
    QVBoxLayout, QStackedWidget, QPushButton, QFormLayout, QLabel, QLineEdit, QDialog
from PyQt5.QtCore import Qt, pyqtSignal
from file_ram_convert.TokenDict import TokenDict


class Token(QWidget):
    begin_save_token_signal = pyqtSignal(str, int)
    token_saved_signal = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(Token, self).__init__(parent=parent)
        v_layout = QVBoxLayout(self)
        v_layout.setContentsMargins(100, 100, 100, 100)
        f_layout = QFormLayout()
        qss_style = '''
            QLineEdit {
                min-width: 250;
            }
            
        '''
        self.setStyleSheet(qss_style)
        self.APPID_line_edit = QLineEdit()
        f_layout.addRow(QLabel("APPID"), self.APPID_line_edit)
        self.APISecret_line_edit = QLineEdit()
        f_layout.addRow(QLabel("APISecret"), self.APISecret_line_edit)
        self.APIKey_line_edit = QLineEdit()
        f_layout.addRow(QLabel("APIKey"), self.APIKey_line_edit)
        self.load_token()

        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton('保存')
        self.btn_save.clicked.connect(self.save_token)
        self.btn_cancel = QPushButton('取消')
        self.btn_cancel.clicked.connect(self.load_token)

        f_widget = QWidget()
        f_widget.setLayout(f_layout)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btn_save)
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addStretch(1)
        btn_widget = QWidget()
        btn_widget.setLayout(btn_layout)
        v_layout.addStretch(1)
        v_layout.addWidget(f_widget)
        v_layout.addWidget(btn_widget)
        v_layout.addStretch(1)
        self.setLayout(v_layout)

    # 得到当前token
    def load_token(self):
        token_loader = TokenDict('../status_saved/aiui.npy')
        token_info = token_loader.load()
        self.APPID_line_edit.setText(token_info["APPID"])
        self.APISecret_line_edit.setText(token_info["APISecret"])
        self.APIKey_line_edit.setText(token_info["APIKey"])

    # 保存token
    def save_token(self):
        self.begin_save_token_signal.emit('正在保存到文件', 3000)
        token_dict = {
            "APPID": self.APPID_line_edit.text(),
            "APISecret": self.APISecret_line_edit.text(),
            "APIKey": self.APIKey_line_edit.text()
        }

        def saver(_dict):
            self.btn_save.setEnabled(False)
            self.btn_cancel.setEnabled(False)
            token_saver = TokenDict('../status_saved/aiui.npy', _dict)
            token_saver.save()
            self.btn_save.setEnabled(True)
            self.btn_cancel.setEnabled(True)
            self.token_saved_signal.emit('修改已保存', 3000)

        thread = Thread(target=saver, args=(token_dict,))
        thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = Token()
    widget.setGeometry(400, 200, 800, 600)
    widget.show()
    sys.exit(app.exec())
