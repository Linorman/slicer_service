import slicer
import time
from PythonQt.QtCore import QModelIndex, Qt
from PythonQt.QtGui import QItemSelectionModel


def addConnector():
    try:
        widget = slicer.util.getModuleWidget('OpenIGTLinkIF')
        addConnectorButton = slicer.util.findChild(widget, "AddConnectorButton")
        addConnectorButton.click()
        b = slicer.mrmlScene.GetNodeByID("vtkMRMLIGTLConnectorNode1")
        b.SetType(1)

        widget = slicer.util.getModuleWidget('OpenIGTLinkIF')
        widget.update()
        prop_status = slicer.util.findChild(widget, "ConnectorStateCheckBox")
        prop_status.setChecked(True)

    except Exception as e:
        print(e)
        return False

    return True


def select_tree_item(tree_view, target_text):
    model = tree_view.model()

    def find_item_index(parent_index, target_text):
        row_count = model.rowCount(parent_index)
        for row in range(row_count):
            index = model.index(row, 0, parent_index)
            item_text = model.data(index)
            if item_text == target_text:
                return index
            found_index = find_item_index(index, target_text)
            if found_index.isValid():
                return found_index
        return QModelIndex()

    root_index = QModelIndex()
    target_index = find_item_index(root_index, target_text)

    if target_index.isValid():
        tree_view.setCurrentIndex(target_index)
        tree_view.selectionModel().select(target_index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
        tree_view.clicked.emit(target_index)
        print(f"Item '{target_text}' selected.")
    else:
        print(f"Item '{target_text}' not found.")

    return target_index


def get_child_items(tree_view, parent_index):
    model = tree_view.model()
    child_items = []
    row_count = model.rowCount(parent_index)
    for row in range(row_count):
        index = model.index(row, 0, parent_index)
        item_text = model.data(index)
        child_items.append(item_text)
    return child_items


def get_child_item_indices(tree_view, parent_index):
    model = tree_view.model()
    child_indices = []
    row_count = model.rowCount(parent_index)
    for row in range(row_count):
        index = model.index(row, 0, parent_index)
        child_indices.append(index)
    return child_indices


def selectIO():
    try:
        widget = slicer.util.getModuleWidget('OpenIGTLinkIF')
        tree = slicer.util.findChild(widget, "IOTreeView")
        target = select_tree_item(tree, "OUT")
        selector = slicer.util.findChild(widget, "NodeSelector")
        selector.setCurrentNodeIndex(3)
        widget = slicer.util.getModuleWidget('OpenIGTLinkIF')
        addBttn = slicer.util.findChild(widget, "AddNodeButton")
        addBttn.click()
        print("IO selected")
        # items = get_child_items(tree, target)
        # target2 = select_tree_item(tree, items[0])
        # model = tree.model()
        # push_on_connect_index = model.index(target2.row(), 4, target2.parent())  # 第五列，索引从0开始
        # if push_on_connect_index.isValid():
        #     model.setData(push_on_connect_index, Qt.Checked, Qt.CheckStateRole)
        #     tree.selectionModel().setCurrentIndex(push_on_connect_index, QItemSelectionModel.ClearAndSelect)
        #     print(f"Checkbox in 'Push On Connect' column for item '{items[0]}' has been checked.")
        # else:
        #     print("Push On Connect index is not valid.")

    except Exception as e:
        print(e)
        return False

    return True
