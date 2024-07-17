import nibabel as nib
import pyvista as pv
import numpy as np
import vtk

# 加载 NIfTI 文件
# nii = nib.load('../Clin_CT_all_bones_CT_301_no_series_description_0000.nii.gz')
nii_name = 'segmentations.nii'
nii = nib.load('../' + nii_name)
data = nii.get_fdata()

# 创建 VTK 图像数据
vtk_data = vtk.vtkImageData()
depthArray = vtk.vtkFloatArray()
depthArray.SetNumberOfComponents(1)
depthArray.SetNumberOfTuples(data.size)
for i, val in enumerate(data.flatten(order='F')):
    depthArray.SetValue(i, val)
vtk_data.SetDimensions(data.shape)
vtk_data.GetPointData().SetScalars(depthArray)

# 使用 Marching Cubes 算法生成表面
mc = vtk.vtkMarchingCubes()
mc.SetInputData(vtk_data)
mc.SetValue(0, 0.5)
mc.Update()

# # 转换为 PyVista 格式
# polydata = pv.wrap(mc.GetOutput())
#
# # 保存为 .obj 文件
# polydata.save('output.obj')

# 获取生成的多边形数据
polydata = mc.GetOutput()

# 应用平滑滤波器
smoothFilter = vtk.vtkSmoothPolyDataFilter()
smoothFilter.SetInputData(polydata)
smoothFilter.SetNumberOfIterations(30)  # 调整迭代次数以平滑模型
smoothFilter.SetRelaxationFactor(0.1)   # 调整放松因子以控制平滑度
smoothFilter.Update()

# 转换为 PyVista 格式
smoothed_polydata = pv.wrap(smoothFilter.GetOutput())

# 保存为 .obj 文件
obj_file = 'smoothed_' + nii_name[:-7] + '.obj'
smoothed_polydata.save(obj_file)
