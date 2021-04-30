"""
历史记录ui
"""
import sys
from threading import Thread
import datetime

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTreeWidget, QSplitter, QTreeWidgetItem, QVBoxLayout, \
    QPushButton, QMessageBox, QTreeWidgetItemIterator

sys.path.append('../..')
from package.file_ram_convert.QTreeWidgetXML import QTreeWidgetXML


class HistoryOrder(QWidget):
    file_path = r'../status_saved/history_order_tree.xml'
    begin_save_tree_signal = pyqtSignal(str, int)
    tree_saved_signal = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(HistoryOrder, self).__init__(parent=parent)
        v_layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Vertical)
        # 删、增、改按钮
        tree_modify_btn_s = QHBoxLayout(self)
        self.delete_btn = QPushButton('清空历史记录')
        self.delete_btn.clicked.connect(self.on_clicked_delete_btn)
        # 烦死了，必须要装到widget
        tree_modify_btn_s_widget = QWidget()
        tree_modify_btn_s_widget.setLayout(tree_modify_btn_s)
        tree_modify_btn_s_widget.setMaximumHeight(50)
        # 指令树
        self.tree = self.load_tree()
        self.tree.expandAll()
        self.tree.setColumnWidth(0, 250)
        self.tree.setColumnWidth(1, 200)

        tree_modify_btn_s.addWidget(self.delete_btn)
        splitter.addWidget(tree_modify_btn_s_widget)
        splitter.addWidget(self.tree)
        v_layout.addWidget(splitter)
        self.setLayout(v_layout)

    # 树生成
    def load_tree(self, file_path: str = None) -> QTreeWidget:
        if file_path is None:
            file_path = self.file_path
        tree_xml = QTreeWidgetXML(header_labels_list=["日期、时间", "指令"], file_path=file_path)
        tree_xml.xml_2_tree()
        return QTreeWidget() if (tree_xml.tree is None) else tree_xml.tree

    # 树节点删除
    def on_clicked_delete_btn(self):
        reply = QMessageBox.warning(self, '警告', '所有历史记录均会被删除，\n一旦清空不可撤销',
                                    QMessageBox.No | QMessageBox.Yes,
                                    QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.tree.clear()
            self.saved_tree()

    # 树节点增加
    def history_recorder(self, order: str):
        self.tree.setCurrentItem(None)
        # 获取当前日期
        today = 'Date-' + datetime.date.today().strftime('%Y%m%d')
        iterator = QTreeWidgetItemIterator(self.tree)
        # 遍历记录树
        while iterator.value():
            item = iterator.value()
            if item.text(0) == today:
                self.tree.setCurrentItem(item)
                break
            iterator.__iadd__(1)
        # 如果没有则添加日期节点
        item = self.tree.currentItem()
        if item is None:
            invisible_root = self.tree.invisibleRootItem()
            today_node = QTreeWidgetItem(invisible_root)
            today_node.setText(0, today)
            self.tree.setCurrentItem(today_node)
            item = self.tree.currentItem()
        node = QTreeWidgetItem(item)
        time = 'Time-' + datetime.datetime.now().strftime('%H.%M.%S')
        node.setText(0, time)
        node.setText(1, order)
        self.tree.setCurrentItem(None)
        self.tree.expandItem(item)
        self.saved_tree()

    # 对树的更改保存到文件中
    def saved_tree(self):
        self.begin_save_tree_signal.emit('历史记录修改正在同步到文件', 3000)

        def handler(file_path: str, tree_widget: QTreeWidget):
            tree_convert = QTreeWidgetXML(header_labels_list=["日期、时间", "指令"], file_path=file_path)
            tree_convert.tree_2_xml(tree_widget)
            self.tree_saved_signal.emit('历史记录修改已同步完成', 3000)

        thread = Thread(target=handler, args=(self.file_path, self.tree))
        thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # custom_font = QFont()
    # custom_font.setPointSize(15)
    # app.setFont(custom_font)
    widget = HistoryOrder()
    widget.setGeometry(400, 200, 800, 600)
    widget.show()
    sys.exit(app.exec())
