import SimpleITK as sitk
import vtk
from vtk.util import numpy_support
import pyvista as pv


# 1. 读取DICOM序列
def read_dicom_series(dicom_dir):
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dicom_dir)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    return image


# 2. 进行重采样以标准化图像尺寸
def resample_image(image, new_spacing=None):
    if new_spacing is None:
        new_spacing = [1.0, 1.0, 1.0]
    resample = sitk.ResampleImageFilter()
    resample.SetInterpolator(sitk.sitkLinear)
    resample.SetOutputSpacing(new_spacing)
    resample.SetOutputOrigin(image.GetOrigin())
    resample.SetOutputDirection(image.GetDirection())

    size = [int(round(osz * spc / nsp)) for osz, spc, nsp in zip(image.GetSize(), image.GetSpacing(), new_spacing)]
    resample.SetSize(size)

    resampled_image = resample.Execute(image)
    return resampled_image


# 3. 中值滤波器以平滑图像
def apply_median_filter(image):
    median_filter = sitk.MedianImageFilter()
    median_filter.SetRadius(2)
    return median_filter.Execute(image)


# 4. 将SimpleITK图像转换为VTK图像
def convert_itk_to_vtk(itk_image):
    np_array = sitk.GetArrayFromImage(itk_image)
    vtk_image = vtk.vtkImageData()

    depth, height, width = np_array.shape
    vtk_image.SetDimensions(width, height, depth)
    vtk_data_array = numpy_support.numpy_to_vtk(np_array.ravel(), deep=True, array_type=vtk.VTK_FLOAT)
    vtk_image.GetPointData().SetScalars(vtk_data_array)

    return vtk_image


# 5. 3D可视化使用VTK
def visualize_vtk_image(vtk_image):
# Apply a threshold to remove the table
    # threshold = vtk.vtkImageThreshold()
    # threshold.SetInputData(vtk_image)
    # # Adjust the threshold values based on your data
    # threshold.ThresholdBetween(-800, 4000)  # Keep values between -500 and 1000
    # threshold.ReplaceInOn()
    # threshold.SetInValue(1)  # Keep these values
    # threshold.ReplaceOutOn()
    # threshold.SetOutValue(0)  # Discard other values (the table)
    # threshold.Update()
    # thresholded_image = threshold.GetOutput()

    volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
    volume_mapper.SetInputData(vtk_image)
    # volume_mapper.SetInputData(thresholded_image)
    volume_mapper.SetBlendModeToComposite()

    # 设置颜色传递函数：为不同的像素值设置对应的颜色
    volume_color = vtk.vtkColorTransferFunction()
    volume_color.AddRGBPoint(-1000, 0.0, 0.0, 0.0)  # 空气：黑色
    volume_color.AddRGBPoint(0, 0.0, 0.0, 0.0)  # 空气/背景：黑色
    volume_color.AddRGBPoint(500, 1.0, 0.5, 0.3)  # 软组织：浅橙色
    volume_color.AddRGBPoint(1000, 1.0, 1.0, 0.9)  # 骨骼：白色

    # 设置不透明度传递函数：为不同的像素值设置不透明度，背景值设置为完全透明
    volume_opacity = vtk.vtkPiecewiseFunction()
    volume_opacity.AddPoint(-1000, 0.0)  # 空气/背景：完全透明
    volume_opacity.AddPoint(0, 0.0)  # 背景：完全透明
    volume_opacity.AddPoint(500, 0.2)  # 软组织：稍微不透明
    volume_opacity.AddPoint(1000, 0.85)  # 骨骼：大部分不透明

    # 创建体属性并设置颜色和不透明度
    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(volume_color)
    volume_property.SetScalarOpacity(volume_opacity)
    volume_property.ShadeOn()
    volume_property.SetInterpolationTypeToLinear()

    # 创建体对象
    volume = vtk.vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)

    # 创建渲染器并添加体对象
    renderer = vtk.vtkRenderer()
    renderer.AddViewProp(volume)
    renderer.SetBackground(0.1, 0.2, 0.3)  # 背景色

    # 创建渲染窗口和交互器
    render_window = vtk.vtkRenderWindow()
    render_window.AddRenderer(renderer)

    render_window_interactor = vtk.vtkRenderWindowInteractor()
    render_window_interactor.SetRenderWindow(render_window)

    # 渲染并开始交互
    render_window.Render()
    render_window_interactor.Initialize()
    render_window_interactor.Start()


# 6. 提取等值面并保存为STL文件
def extract_and_save_surface(vtk_image, isovalue=500, output_file="output_model.stl"):
    # 提取等值面
    marching_cubes = vtk.vtkMarchingCubes()
    marching_cubes.SetInputData(vtk_image)
    marching_cubes.SetValue(0, isovalue)
    marching_cubes.Update()

    # 保存为STL文件
    stl_writer = vtk.vtkSTLWriter()
    stl_writer.SetFileName(output_file)
    stl_writer.SetInputConnection(marching_cubes.GetOutputPort())
    stl_writer.Write()

    print(f"Model saved as {output_file}")


# 6. 提取等值面并保存为OBJ文件
def extract_and_save_surface_as_obj(vtk_image, isovalue=500, output_file="output_model.obj"):
    # # 提取等值面
    # marching_cubes = vtk.vtkMarchingCubes()
    # marching_cubes.SetInputData(vtk_image)
    # marching_cubes.SetValue(0, isovalue)
    # marching_cubes.Update()

    # GPU acceleration
    marching_cubes = vtk.vtkFlyingEdges3D()
    marching_cubes.SetInputData(vtk_image)
    marching_cubes.SetValue(0, isovalue)
    marching_cubes.Update()

    # 保存为OBJ文件
    obj_writer = vtk.vtkOBJWriter()
    obj_writer.SetFileName(output_file)
    obj_writer.SetInputConnection(marching_cubes.GetOutputPort())
    obj_writer.Write()

    print(f"Model saved as {output_file}")


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
    decimate.SetTargetReduction(0.9)  # 设置为尽可能高的简化比例
    decimate.Update()
    decimated_polydata = decimate.GetOutput()

    # 获取简化后模型的面片数量
    decimated_num_faces = decimated_polydata.GetNumberOfCells()
    print(f"Decimated number of faces: {decimated_num_faces}")

    # 保存最终简化后的模型
    pv.wrap(decimated_polydata).save(output_path)

    return original_num_faces, decimated_num_faces


def vtk_workflow(dicom_dir, output_file):
    # 读取DICOM序列
    image = read_dicom_series(dicom_dir)

    # 重采样图像
    resampled_image = resample_image(image, [1.0, 1.0, 1.0])

    # 应用中值滤波器
    filtered_image = apply_median_filter(resampled_image)

    # 将SimpleITK图像转换为VTK图像
    vtk_image = convert_itk_to_vtk(filtered_image)

    # 提取等值面并保存为OBJ模型
    extract_and_save_surface_as_obj(vtk_image, isovalue=215, output_file=output_file)

    # 优化模型
    simplify_model(output_file, output_file)

    return output_file


# 主程序
if __name__ == "__main__":
    # 替换为你自己的DICOM目录路径
    dicom_directory = r"E:\Lenevo\Desktop\workspace\ct\dicom"

    # 读取DICOM序列
    image = read_dicom_series(dicom_directory)

    # 重采样图像
    resampled_image = resample_image(image, [1.0, 1.0, 1.0])

    # 应用中值滤波器
    filtered_image = apply_median_filter(resampled_image)

    # 将SimpleITK图像转换为VTK图像
    vtk_image = convert_itk_to_vtk(filtered_image)

    # 可视化
    visualize_vtk_image(vtk_image)

    # # 提取等值面并保存为OBJ模型
    # extract_and_save_surface_as_obj(vtk_image, isovalue=215, output_file="../simpleitk-test/output_model.obj")
