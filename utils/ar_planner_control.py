import slicer

widget = slicer.util.getModuleWidget('AR_Planner')


def editInputVolumePath(path):
    try:
        widget.ui.inputVolumePath.setCurrentPath(path)
        widget.ui.loadInputVolumeButton.click()
    except Exception as e:
        print(e)
        return False
    return True


def editInputSelector():
    try:
        widget.ui.createImageSliceButton.click()
    except Exception as e:
        print(e)
        return False
    return True
