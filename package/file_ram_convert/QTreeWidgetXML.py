"""
从XML文件中提取树，并把树储存到XML文件中
"""
import sys
from os.path import exists
from xml.etree import ElementTree

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QMainWindow


class QTreeWidgetXML:
    tree: QTreeWidget = None
    file_path: str = None

    def __init__(self, header_labels_list: dict, file_path: str):
        if exists(file_path):
            self.file_path = file_path
        else:
            print('XML文件不存在')
        self.header_labels_list = header_labels_list
        self.columnNum = len(header_labels_list)

    # 从XML文件中读取树
    def xml_2_tree(self, file_path: str = None):
        if file_path is None:
            file_path = self.file_path
        if self.file_path is None:
            print('先指定XML文件')
            return
        element_tree = ElementTree.parse(file_path)
        root_elem = element_tree.getroot()

        # 生成树
        def tree_widget_generator(tree_elem: ElementTree.Element, tree_item: QTreeWidgetItem):
            tree_item.setText(0, tree_elem.tag)
            for i in range(1, self.columnNum):
                tree_item.setText(
                    i,
                    tree_elem.attrib[self.header_labels_list[i]] if (
                            self.header_labels_list[i] in tree_elem.attrib.keys()
                    ) else ''
                )
            for child_elem in tree_elem:
                child_item = QTreeWidgetItem(tree_item)
                tree_widget_generator(child_elem, child_item)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(self.columnNum)
        header_labels = list()
        for i in range(self.columnNum):
            header_labels.append(self.header_labels_list[i])
        self.tree.setHeaderLabels(header_labels)
        tree_widget_generator(root_elem, self.tree.invisibleRootItem())

    # 保存树到XML文件
    def tree_2_xml(self, tree_widget: QTreeWidget = None, save_as: str = None):
        if tree_widget is None:
            tree_widget = self.tree
        if not save_as:
            save_as = self.file_path
        if (tree_widget is None) or (save_as is None):
            return
        root_item = tree_widget.invisibleRootItem()
        root_elem = ElementTree.Element('root')

        def tree_elem_generator(tree_elem: ElementTree.Element, tree_item: QTreeWidgetItem):
            for i in range(tree_item.childCount()):
                child_item = tree_item.child(i)
                attrib = dict()
                for i in range(1, self.columnNum):
                    if child_item.text(i):
                        attrib[self.header_labels_list[i]] = child_item.text(i)
                child_elem = ElementTree.SubElement(
                    tree_elem,
                    child_item.text(0),
                    attrib=attrib
                )
                tree_elem_generator(child_elem, child_item)

        tree_elem_generator(root_elem, root_item)
        tree = ElementTree.ElementTree(root_elem)
        tree.write(save_as, encoding='utf-8')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    custom_font = QFont()
    custom_font.setPointSize(18)
    app.setFont(custom_font)

    tree_xml = QTreeWidgetXML(header_labels_list=['名称', '指令', '备注'], file_path=r'../status_saved/saved_order_tree.xml')
    tree_xml.xml_2_tree()
    tree_xml.tree_2_xml()

    widget = QMainWindow()
    widget.setCentralWidget(tree_xml.tree)
    tree_xml.tree.expandAll()
    tree_xml.tree.setColumnWidth(1, 150)
    widget.setGeometry(400, 200, 800, 600)
    widget.show()
    sys.exit(app.exec())
