from utils.seg import segmentation
from utils.nii_2_obj import nii_2_obj, nii_list_2_obj, simplify_model

if __name__ == "__main__":
    input_path = "./CT_301_no_series_description_0000.nii.gz"
    output_path = "./output/segmentation.nii.gz"
    output_obj = "./output/segmentation.obj"
    # segmentation(input_path, output_path)
    output_path = "./segmentations.nii"
    input_obj = "./bones.obj"
    output_obj = "./brain.obj"
    nii_2_obj(output_path, output_obj)
    # simplify_model(input_obj, output_obj, 10)

    # nii_list = ["./appendicular_bones.nii", "./segmentations.nii"]
    # output_obj = "./bones.obj"
    # nii_list_2_obj(nii_list, output_obj)
