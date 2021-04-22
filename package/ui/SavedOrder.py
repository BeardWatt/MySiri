"""
已存记录ui
"""
import sys
from threading import Thread

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QTreeWidget, QSplitter, QTreeWidgetItem, QVBoxLayout, \
    QPushButton, QMessageBox, QDialog

from package.voice_function import W2V as W2V
from SavedOrderChangeDialog import SavedOrderChangeDialog
from package.file_ram_convert.QTreeWidgetXML import QTreeWidgetXML
from package.voice_function.MP3Player import MP3Player
from package.voice_function.TuringRobot import TuringRobot


class SavedOrder(QWidget):
    file_path = r'../status_saved/saved_order_tree.xml'
    begin_save_tree_signal = pyqtSignal(str, int)
    tree_saved_signal = pyqtSignal(str, int)

    def __init__(self, parent=None):
        super(SavedOrder, self).__init__(parent=parent)
        v_layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Vertical)
        # 删、增、改按钮
        tree_modify_btn_s = QHBoxLayout(self)
        self.delete_btn = QPushButton('删除')
        self.delete_btn.clicked.connect(self.on_clicked_delete_btn)
        self.add_btn = QPushButton('增加')
        self.add_btn.clicked.connect(self.on_clicked_add_btn)
        self.change_btn = QPushButton('修改')
        self.change_btn.clicked.connect(self.on_clicked_change_btn)
        # 烦死了，必须要装到widget
        tree_modify_btn_s_widget = QWidget()
        tree_modify_btn_s_widget.setLayout(tree_modify_btn_s)
        tree_modify_btn_s_widget.setMaximumHeight(50)
        # 指令树
        self.tree = self.load_tree()
        self.tree.expandAll()
        self.tree.setColumnWidth(0, 150)
        self.tree.setColumnWidth(1, 200)
        self.tree.currentItemChanged.connect(self.on_changed_tree_item)
        # 运行
        self.run_btn = QPushButton('执行')
        self.run_btn.clicked.connect(self.on_clicked_run)

        tree_modify_btn_s.addWidget(self.delete_btn)
        tree_modify_btn_s.addStretch(1)
        tree_modify_btn_s.addWidget(self.add_btn)
        tree_modify_btn_s.addWidget(self.change_btn)
        splitter.addWidget(tree_modify_btn_s_widget)
        splitter.addWidget(self.tree)
        splitter.addWidget(self.run_btn)
        v_layout.addWidget(splitter)
        self.on_changed_tree_item()
        self.setLayout(v_layout)

    # 树生成
    def load_tree(self, file_path: str = None) -> QTreeWidget:
        if file_path is None:
            file_path = self.file_path
        tree_xml = QTreeWidgetXML(file_path=file_path)
        tree_xml.xml_2_tree()
        return QTreeWidget() if (tree_xml.tree is None) else tree_xml.tree

    # 树节点删除
    def on_clicked_delete_btn(self):
        item = self.tree.currentItem()
        if item is None:
            return
        invisible_root = self.tree.invisibleRootItem()
        reply = QMessageBox.warning(self, '警告', '该节点及其下所有节点均会被删除，\n一旦删除不可撤销',
                                    QMessageBox.No | QMessageBox.Yes,
                                    QMessageBox.No)
        if reply == QMessageBox.Yes:
            for item in self.tree.selectedItems():
                (item.parent() or invisible_root).removeChild(item)
        self.tree.setCurrentItem(None)
        self.saved_tree()

    # 树节点增加
    def on_clicked_add_btn(self):
        item = self.tree.currentItem()
        invisible_root = self.tree.invisibleRootItem()
        node = QTreeWidgetItem(item or invisible_root)
        node.setText(0, 'temp')
        self.tree.setCurrentItem(None)
        self.saved_tree()

    # 树节点修改
    def on_clicked_change_btn(self):
        item = self.tree.currentItem()
        if item is None:
            return
        dialog = SavedOrderChangeDialog(self, name=item.text(0), order=item.text(1), desc=item.text(2))
        result = dialog.exec()
        if result == QDialog.Accepted:
            name, order, desc = dialog.get_info()
            item.setText(0, name)
            item.setText(1, order)
            item.setText(2, desc)
            self.saved_tree()
        self.tree.setCurrentItem(None)

    # 对树的更改保存到文件中
    def saved_tree(self):
        self.begin_save_tree_signal.emit('正在保存到文件', 3000)

        def handler(file_path: str, tree_widget: QTreeWidget):
            tree_convert = QTreeWidgetXML(file_path=file_path)
            tree_convert.tree_2_xml(tree_widget)
            self.tree_saved_signal.emit('修改已保存', 3000)

        thread = Thread(target=handler, args=(self.file_path, self.tree))
        thread.start()

    # 当前tree_item改变
    def on_changed_tree_item(self):
        item = self.tree.currentItem()
        if item is None:
            self.delete_btn.setEnabled(False)
            self.change_btn.setEnabled(False)
        else:
            self.delete_btn.setEnabled(True)
            self.change_btn.setEnabled(True)
        if (item is None) or (not item.text(1)):
            self.run_btn.setEnabled(False)
        else:
            self.run_btn.setEnabled(True)

    def on_clicked_run(self):
        self.tree.setEnabled(False)
        self.run_btn.setEnabled(False)

        def handler():
            turing_robot = TuringRobot(self.tree.currentItem().text(1))
            respond_text = turing_robot.get_respond()
            gap = W2V.get_voice(respond_text)
            mp3_player = MP3Player(r'../voice_cache/w2v.mp3')
            mp3_player.player()
            self.tree.setEnabled(True)
            self.tree.setCurrentItem(None)
            self.run_btn.setEnabled(True)

        thread = Thread(target=handler)
        thread.start()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # custom_font = QFont()
    # custom_font.setPointSize(15)
    # app.setFont(custom_font)
    widget = SavedOrder()
    widget.setGeometry(400, 200, 800, 600)
    widget.show()
    sys.exit(app.exec())
