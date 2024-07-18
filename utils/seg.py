import nibabel as nib
from totalsegmentator.python_api import totalsegmentator


def segmentation(input_path, output_path):
    roi_subset = [
        "vertebrae_S1", "vertebrae_L5", "vertebrae_L4", "vertebrae_L3", "vertebrae_L2",
        "vertebrae_L1", "vertebrae_T12", "vertebrae_T11", "vertebrae_T10", "vertebrae_T9",
        "vertebrae_T8", "vertebrae_T7", "vertebrae_T6", "vertebrae_T5", "vertebrae_T4",
        "vertebrae_T3", "vertebrae_T2", "vertebrae_T1", "vertebrae_C7", "vertebrae_C6",
        "vertebrae_C5", "vertebrae_C4", "vertebrae_C3", "vertebrae_C2", "vertebrae_C1",
        "sacrum", "spinal_cord"
    ]
    ret = totalsegmentator(input_path, output_path, roi_subset_robust=roi_subset, ml=True)
    if ret is None:
        return False
    else:
        return True


def segmentation_nii(input_img, output_img):
    roi_subset = [
        "vertebrae_S1", "vertebrae_L5", "vertebrae_L4", "vertebrae_L3", "vertebrae_L2",
        "vertebrae_L1", "vertebrae_T12", "vertebrae_T11", "vertebrae_T10", "vertebrae_T9",
        "vertebrae_T8", "vertebrae_T7", "vertebrae_T6", "vertebrae_T5", "vertebrae_T4",
        "vertebrae_T3", "vertebrae_T2", "vertebrae_T1", "vertebrae_C7", "vertebrae_C6",
        "vertebrae_C5", "vertebrae_C4", "vertebrae_C3", "vertebrae_C2", "vertebrae_C1",
        "sacrum", "spinal_cord"
    ]
    return totalsegmentator(input_img, roi_subset_robust=roi_subset, ml=True)


if __name__ == "__main__":
    input_path = "../Clin_CT_all_bones_CT_301_no_series_description_0000.nii.gz"
    output_path = "../segmentation.nii.gz"
    segmentation(input_path, output_path)
