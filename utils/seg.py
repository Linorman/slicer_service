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


def segmentation_leg(input_path, output_path):
    roi_subset = [
        "femur_L", "femur_R", "tibia_L", "tibia_R", "fibula_L", "fibula_R", "patella_L", "patella_R"
    ]


import subprocess


def run_totalsegmentator(input_file, output_dir, roi_subset=None, task=None, use_ml=True):
    command = ["TotalSegmentator", "-i", input_file, "-o", output_dir]

    if roi_subset:
        command.extend(["--roi_subset"] + roi_subset)
    if task:
        command.extend(["--task", task])
    if use_ml:
        command.append("--ml")

    subprocess.run(command, check=True)


if __name__ == "__main__":
    input_path = "../patient1.nii.gz"
    output_path1 = "../roi_subset.nii.gz"
    output_path2 = "../appendicular_bones.nii.gz"
    # segmentation(input_path, output_path)
    # 运行第一个指令
    roi_subset = ["femur_left", "femur_right", "hip_left", "hip_right"]
    run_totalsegmentator(input_path, output_path1, roi_subset=roi_subset)

    # 运行第二个指令
    task = "appendicular_bones"
    run_totalsegmentator(input_path, output_path2, task=task)
