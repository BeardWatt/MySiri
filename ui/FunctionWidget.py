"""
功能区ui
"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTreeWidget, QSplitter, QTreeWidgetItem, QStackedWidget
from PyQt5.QtCore import Qt, pyqtSignal
from NewOrder import NewOrder
from SavedOrder import SavedOrder
from Token import Token


class FunctionWidget(QWidget):
    begin_save_signal = pyqtSignal(str, int)
    saved_signal = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(FunctionWidget, self).__init__(parent=parent)
        h_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        # 功能树
        self.tree = QTreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setFixedWidth(160)
        self.tree.setHeaderLabel("功能选项")
        # 交互——树节点
        react = QTreeWidgetItem(self.tree)
        react.setText(0, "交互")
        new_order = QTreeWidgetItem(react)
        new_order.setText(0, "新指令")
        saved_order = QTreeWidgetItem(react)
        saved_order.setText(0, "已存记录")
        # 设置——树节点
        setting = QTreeWidgetItem(self.tree)
        setting.setText(0, "设置")
        token = QTreeWidgetItem(setting)
        token.setText(0, "讯飞Token")
        # 树操作
        self.tree.expandAll()
        self.tree.currentItemChanged.connect(self.on_clicked_tree)
        # 功能界面栈
        self.stack = QStackedWidget()
        self.stack.setMinimumWidth(380)
        # 功能界面
        self.stack_new_order = NewOrder()
        self.stack_saved_order = SavedOrder()
        self.stack_saved_order.begin_save_tree_signal.connect(self.handle_begin_save)
        self.stack_saved_order.tree_saved_signal.connect(self.handle_saved)
        self.stack_token = Token()
        self.stack_token.begin_save_token_signal.connect(self.handle_begin_save)
        self.stack_token.token_saved_signal.connect(self.handle_saved)
        self.stack.addWidget(self.stack_new_order)
        self.stack.addWidget(self.stack_saved_order)
        self.stack.addWidget(self.stack_token)

        splitter.addWidget(self.tree)
        splitter.addWidget(self.stack)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 6)
        h_layout.addWidget(splitter)
        self.setLayout(h_layout)

    # 切换功能界面栈的界面
    def on_clicked_tree(self, item: QTreeWidgetItem):
        text = item.text(0)
        if text == "新指令" or text == "交互":
            self.stack.setCurrentIndex(0)
        elif text == "已存记录":
            self.stack.setCurrentIndex(1)
        elif text == "讯飞Token" or text == "设置":
            self.stack.setCurrentIndex(2)

    # 已存指令树：开始保存
    def handle_begin_save(self, s: str, duration: int):
        self.begin_save_signal.emit(s, duration)

    # 已存指令树：已保存
    def handle_saved(self, s: str, duration: int):
        self.saved_signal.emit(s, duration)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = FunctionWidget()
    widget.setGeometry(400, 200, 800, 600)
    widget.show()
    sys.exit(app.exec())
