import os
import nibabel as nib
import nrrd
import pyvista as pv
import numpy as np
import pydicom
import vtk


def nrrd_2_nifti(nrrd_file, output_file):
    data, header = nrrd.read(nrrd_file)

    spacing = header.get('space directions')
    if spacing is None:
        spacing = header.get('spacings')
    if spacing is None:
        raise ValueError("NRRD文件中没有找到空间方向或间距信息")

    affine = nib.affines.from_matvec(spacing)

    # 创建NIfTI图像
    nifti_image = nib.Nifti1Image(data, affine)

    # 保存为.nii.gz文件
    nib.save(nifti_image, output_file)
    print(f"转换完成: {output_file}")


def dicom_2_nifti(dicom_dir, output_file):
    dicom_files = [os.path.join(dicom_dir, f) for f in os.listdir(dicom_dir) if f.endswith('.dcm')]

    dicoms = [pydicom.dcmread(f) for f in sorted(dicom_files)]

    slices = [d.pixel_array for d in dicoms]
    image_array = np.stack(slices, axis=-1)

    affine = np.eye(4)
    affine[0, 0] = dicoms[0].PixelSpacing[0]
    affine[1, 1] = dicoms[0].PixelSpacing[1]
    affine[2, 2] = dicoms[0].SliceThickness

    nifti_image = nib.Nifti1Image(image_array, affine)

    # 保存为.nii.gz文件
    nib.save(nifti_image, output_file)
    print(f"转换完成: {output_file}")


def nii_2_obj(nii_path, obj_path):
    nii = nib.load(nii_path)
    data = nii.get_fdata()

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
