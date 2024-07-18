import os

import flask
from flask import request, jsonify

from utils.ar_planner_control import editInputVolumePath, editInputSelector
from utils.igt_control import addConnector, selectIO
from utils.seg import segmentation
from utils.nii_2_obj import nii_2_obj, nrrd_2_nifti

app = flask.Flask(__name__)


@app.route('/upload', methods=['Post'])
def upload(path):
    return editInputVolumePath(path)


@app.route('/createReslice', methods=['POST'])
def createReslice():
    return editInputSelector()


@app.route('/initIGT', methods=['POST'])
def initIGT():
    tag1 = addConnector()
    tag2 = selectIO()
    return tag1 and tag2


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
    app.run()
