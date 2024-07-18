import os
import nibabel as nib
import pyvista as pv
import numpy as np
import vtk


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
