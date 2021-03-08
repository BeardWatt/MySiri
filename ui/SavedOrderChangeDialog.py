"""
点击修改按钮时弹出的对话框
"""
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QFormLayout, QLabel, QLineEdit, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class SavedOrderChangeDialog(QDialog):
    def __init__(self, parent=None, name: str = '', order: str = '', desc: str = ''):
        super(SavedOrderChangeDialog, self).__init__(parent=parent)
        self.setWindowTitle('修改指令信息')
        layout = QFormLayout()
        self.name_edit = QLineEdit(name)
        self.order_edit = QLineEdit(order)
        self.desc_edit = QLineEdit(desc)
        buttons = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok, Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addRow(QLabel('名称'), self.name_edit)
        layout.addRow(QLabel('指令'), self.order_edit)
        layout.addRow(QLabel('备注'), self.desc_edit)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_info(self):
        return self.name_edit.text(), self.order_edit.text(), self.desc_edit.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # custom_font = QFont()
    # custom_font.setPointSize(15)
    # app.setFont(custom_font)
    widget = SavedOrderChangeDialog()
    # widget.setGeometry(400, 200, 800, 600)
    widget.show()
    sys.exit(app.exec())
