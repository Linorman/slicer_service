from utils.ar_planner_control import editInputVolumePath, editInputSelector
from utils.igt_control import addConnector, selectIO

path = r"E:\Lenevo\Desktop\slicer_service\Patient001-CT_cropped.nrrd"
ret = editInputVolumePath(path)
if not ret:
    print("editInputVolumePath failed.")
    # exit(1)

ret = editInputSelector()
if not ret:
    print("editInputSelector failed.")
    # exit(1)

tag1 = addConnector()
if not tag1:
    print("addConnector failed.")
    # exit(1)
tag2 = selectIO()
if not tag2:
    print("selectIO failed.")
    # exit(1)

print("All operations are successful.")
