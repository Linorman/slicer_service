import slicer
from PythonQt.QtCore import QModelIndex, Qt
from PythonQt.QtGui import QItemSelectionModel

widget = slicer.util.getModuleWidget('OpenIGTLinkIF')


def addConnector():
    try:
        addConnectorButton = slicer.util.findChild(widget, "AddConnectorButton")
        addConnectorButton.click()
        prop_type = slicer.util.findChild(widget, "ConnectorServerRadioButton")
        prop_type.setChecked(True)

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
        tree = slicer.util.findChild(widget, "IOTreeView")
        target = select_tree_item(tree, "OUT")
        addBttn = slicer.util.findChild(widget, "AddNodeButton")
        addBttn.click()
        items = get_child_items(tree, target)
        target2 = select_tree_item(tree, items[0])
        model = tree.model()
        push_on_connect_index = model.index(target2.row(), 4, target2.parent())  # 第五列，索引从0开始
        if push_on_connect_index.isValid():
            model.setData(push_on_connect_index, Qt.Checked, Qt.CheckStateRole)
            tree.selectionModel().setCurrentIndex(push_on_connect_index, QItemSelectionModel.ClearAndSelect)
            print(f"Checkbox in 'Push On Connect' column for item '{items[0]}' has been checked.")
        else:
            print("Push On Connect index is not valid.")

        # sendBttn = slicer.util.findChild(widget, "SendButton")
        # sendBttn.click()

    except Exception as e:
        print(e)
        return False

    return True
