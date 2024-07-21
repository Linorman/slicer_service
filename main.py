import os

import flask
from flask import request, jsonify

from utils.seg import segmentation
from utils.nii_2_obj import nii_2_obj, nrrd_2_nifti

app = flask.Flask(__name__)


@app.route('/seg', methods=['POST'])
def seg():
    input_path = request.json['input_path']
    output_dir = '/home/nii'
    file_name = os.path.splitext(os.path.basename(input_path))[0]
    nrrd_dir = '/home/nrrd'
    nrrd_path = os.path.join(nrrd_dir, file_name + ".nrrd")
    nii_path = os.path.join(output_dir, file_name + ".nii.gz")
    nrrd_2_nifti(nrrd_path, nii_path)
    output_path = os.path.join(output_dir, file_name + '-seg.nii.gz')

    ret = segmentation(nii_path, output_path)
    if ret:
        obj_path = os.path.join('/home/obj', file_name + '.obj')
        nii_2_obj(output_path, obj_path)
        return jsonify(obj_path=obj_path)
    else:
        return jsonify(error="Segmentation failed"), 500


if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port)
