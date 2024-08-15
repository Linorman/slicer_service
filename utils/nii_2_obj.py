import nibabel as nib
import numpy as np
import pyvista as pv
import vtk
import SimpleITK as sitk
import os


def dicom_to_nifti(dicom_folder, output_file):
    # 读取 DICOM 文件夹中的所有 DICOM 文件
    reader = sitk.ImageSeriesReader()
    dicom_series = reader.GetGDCMSeriesFileNames(dicom_folder)
    reader.SetFileNames(dicom_series)

    # 读取 DICOM 文件并转换为 SimpleITK 图像
    image = reader.Execute()

    # 保存为 NIfTI 文件
    sitk.WriteImage(image, output_file)


def nii_2_obj(nii_path, obj_path):
    nii = nib.load(nii_path)
    data = nii.get_fdata()
    print("loading data ......")

    vtk_data = vtk.vtkImageData()
    depthArray = vtk.vtkFloatArray()
    depthArray.SetNumberOfComponents(1)
    depthArray.SetNumberOfTuples(data.size)
    for i, val in enumerate(data.flatten(order='F')):
        depthArray.SetValue(i, val)
    vtk_data.SetDimensions(data.shape)
    vtk_data.GetPointData().SetScalars(depthArray)

    mc = vtk.vtkMarchingCubes()
    mc.SetInputData(vtk_data)
    mc.SetValue(0, 0.5)
    mc.Update()

    polydata = mc.GetOutput()

    smoothFilter = vtk.vtkSmoothPolyDataFilter()
    smoothFilter.SetInputData(polydata)
    smoothFilter.SetNumberOfIterations(30)
    smoothFilter.SetRelaxationFactor(0.1)
    smoothFilter.Update()

    smoothed_polydata = pv.wrap(smoothFilter.GetOutput())
    smoothed_polydata.save(obj_path)


def nii_2_obj_sim(nii_path, obj_path, reduction=0.5):
    nii = nib.load(nii_path)
    data = nii.get_fdata()
    print("loading data ......")

    vtk_data = vtk.vtkImageData()
    depthArray = vtk.vtkFloatArray()
    depthArray.SetNumberOfComponents(1)
    depthArray.SetNumberOfTuples(data.size)
    for i, val in enumerate(data.flatten(order='F')):
        depthArray.SetValue(i, val)
    vtk_data.SetDimensions(data.shape)
    vtk_data.GetPointData().SetScalars(depthArray)

    mc = vtk.vtkMarchingCubes()
    mc.SetInputData(vtk_data)
    mc.SetValue(0, 0.5)  # 可以调整阈值
    mc.Update()

    polydata = mc.GetOutput()

    # 添加简化过滤器
    decimate = vtk.vtkDecimatePro()
    decimate.SetInputData(polydata)
    decimate.SetTargetReduction(reduction)  # 设置简化比率 (0.0 - 1.0)
    decimate.PreserveTopologyOn()
    decimate.Update()

    simplified_polydata = decimate.GetOutput()

    smoothFilter = vtk.vtkSmoothPolyDataFilter()
    smoothFilter.SetInputData(simplified_polydata)
    smoothFilter.SetNumberOfIterations(15)  # 可以减少迭代次数
    smoothFilter.SetRelaxationFactor(0.1)
    smoothFilter.Update()

    smoothed_polydata = pv.wrap(smoothFilter.GetOutput())
    smoothed_polydata.save(obj_path)


def simplify_model(input_path, output_path, reduction=0.5):
    reader = vtk.vtkOBJReader()
    reader.SetFileName(input_path)
    reader.Update()
    input_polydata = reader.GetOutput()

    # 获取原始模型的面片数量
    original_num_faces = input_polydata.GetNumberOfCells()
    print(f"Original number of faces: {original_num_faces}")

    # 清理数据
    clean_filter = vtk.vtkCleanPolyData()
    clean_filter.SetInputData(input_polydata)
    clean_filter.Update()
    clean_polydata = clean_filter.GetOutput()

    # 简化模型
    decimate = vtk.vtkQuadricDecimation()
    decimate.SetInputData(clean_polydata)
    decimate.SetTargetReduction(0.97)  # 设置为尽可能高的简化比例
    decimate.Update()
    decimated_polydata = decimate.GetOutput()

    # 获取简化后模型的面片数量
    decimated_num_faces = decimated_polydata.GetNumberOfCells()
    print(f"Decimated number of faces: {decimated_num_faces}")

    # 进一步处理（如光滑过滤器）
    smooth_filter = vtk.vtkSmoothPolyDataFilter()
    smooth_filter.SetInputData(decimated_polydata)
    smooth_filter.SetNumberOfIterations(5)  # 可以减少迭代次数以保持更多细节
    smooth_filter.SetRelaxationFactor(0.1)
    smooth_filter.Update()
    smoothed_polydata = smooth_filter.GetOutput()

    # 获取光滑后模型的面片数量
    smoothed_num_faces = smoothed_polydata.GetNumberOfCells()
    print(f"Smoothed number of faces: {smoothed_num_faces}")

    # 保存最终简化后的模型
    pv.wrap(smoothed_polydata).save(output_path)

    return original_num_faces, decimated_num_faces, smoothed_num_faces


def nii_list_2_obj(nii_paths, obj_path):
    # Load and combine NIfTI data
    nii_data = [nib.load(nii_path).get_fdata() for nii_path in nii_paths]
    combined_data = np.stack(nii_data, axis=-1)  # Stack along the new fourth dimension
    combined_data_3d = np.mean(combined_data, axis=-1)  # Average along the fourth dimension to get 3D data

    print("Loading and combining data ......")

    # Prepare VTK data
    vtk_data = vtk.vtkImageData()
    depthArray = vtk.vtkFloatArray()
    depthArray.SetNumberOfComponents(1)
    depthArray.SetNumberOfTuples(combined_data_3d.size)
    for i, val in enumerate(combined_data_3d.flatten(order='F')):
        depthArray.SetValue(i, val)
    vtk_data.SetDimensions(combined_data_3d.shape)
    vtk_data.GetPointData().SetScalars(depthArray)

    # Apply Marching Cubes
    mc = vtk.vtkMarchingCubes()
    mc.SetInputData(vtk_data)
    mc.SetValue(0, 0.5)
    mc.Update()

    polydata = mc.GetOutput()

    # Save the result
    polydata = pv.wrap(polydata)
    polydata.save(obj_path)
