"""
功能区ui
"""
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTreeWidget, QSplitter, QTreeWidgetItem, QStackedWidget

from NewOrder import NewOrder
from SavedOrder import SavedOrder
from HistoryOrder import HistoryOrder
from Token import Token
from TuringRobotToken import TuringRobotToken
from TXT2V import TXT2V
from V2TXT import V2TXT


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
        age_sex_identification = QTreeWidgetItem(react)
        age_sex_identification.setText(0, "年龄、性别识别")
        emotion_analysis = QTreeWidgetItem(react)
        emotion_analysis.setText(0, "情感分析")
        saved_order = QTreeWidgetItem(react)
        saved_order.setText(0, "已存指令")
        history_order = QTreeWidgetItem(react)
        history_order.setText(0, "历史记录")
        txt2v = QTreeWidgetItem(react)
        txt2v.setText(0, "文字转语音")
        v2txt = QTreeWidgetItem(react)
        v2txt.setText(0, "语音转文字")
        # 设置——树节点
        setting = QTreeWidgetItem(self.tree)
        setting.setText(0, "设置")
        token = QTreeWidgetItem(setting)
        token.setText(0, "讯飞Token")
        turing_robot_token = QTreeWidgetItem(setting)
        turing_robot_token.setText(0, "图灵机器人Token")
        # 树操作
        self.tree.expandAll()
        self.tree.currentItemChanged.connect(self.on_clicked_tree)
        # 功能界面栈
        self.stack = QStackedWidget()
        self.stack.setMinimumWidth(380)
        # 功能界面
        stack_new_order = NewOrder(title_text='新指令')
        stack_age_sex_identification = NewOrder(title_text='年龄、性别识别')
        stack_emotion_analysis = NewOrder(title_text='情感分析')
        stack_saved_order = SavedOrder()
        stack_saved_order.begin_save_tree_signal.connect(self.handle_begin_save)
        stack_saved_order.tree_saved_signal.connect(self.handle_saved)
        stack_history_order = HistoryOrder()
        stack_history_order.begin_save_tree_signal.connect(self.handle_begin_save)
        stack_history_order.tree_saved_signal.connect(self.handle_saved)
        stack_new_order.begin_record_order_signal.connect(stack_history_order.history_recorder)
        stack_saved_order.begin_record_order_signal.connect(stack_history_order.history_recorder)
        stack_txt2v = TXT2V()
        stack_v2txt = V2TXT()
        stack_token = Token()
        stack_token.begin_save_token_signal.connect(self.handle_begin_save)
        stack_token.token_saved_signal.connect(self.handle_saved)
        stack_turing_robot_token = TuringRobotToken()
        stack_turing_robot_token.begin_save_token_signal.connect(self.handle_begin_save)
        stack_turing_robot_token.token_saved_signal.connect(self.handle_saved)
        self.stack.addWidget(stack_new_order)
        self.stack.addWidget(stack_age_sex_identification)
        self.stack.addWidget(stack_emotion_analysis)
        self.stack.addWidget(stack_saved_order)
        self.stack.addWidget(stack_history_order)
        self.stack.addWidget(stack_txt2v)
        self.stack.addWidget(stack_v2txt)
        self.stack.addWidget(stack_token)
        self.stack.addWidget(stack_turing_robot_token)

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
        elif text == "年龄、性别识别":
            self.stack.setCurrentIndex(1)
        elif text == "情感分析":
            self.stack.setCurrentIndex(2)
        elif text == "已存指令":
            self.stack.setCurrentIndex(3)
        elif text == "历史记录":
            self.stack.setCurrentIndex(4)
        elif text == "文字转语音":
            self.stack.setCurrentIndex(5)
        elif text == "语音转文字":
            self.stack.setCurrentIndex(6)
        elif text == "讯飞Token" or text == "设置":
            self.stack.setCurrentIndex(7)
        elif text == "图灵机器人Token":
            self.stack.setCurrentIndex(8)

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
