import os

import flask
from flask import request, jsonify

from utils.seg import segmentation, seg_workflow
from utils.dicom23d import vtk_workflow
import logging

app = flask.Flask(__name__)


@app.route('/seg', methods=['POST'])
def seg():
    dcm_path = request.json['dcm_path']
    obj_path = request.json['obj_path']
    nii_path = request.json['nii_path']

    # change path from ubuntu to windows
    dcm_path = dcm_path.replace("/home/work-temp", "Y:").replace("/", "\\")
    obj_path = obj_path.replace("/home/work-temp", "Y:").replace("/", "\\")
    nii_path = nii_path.replace("/home/work-temp", "Y:").replace("/", "\\")

    logging.debug(f"DCM Path: {dcm_path}")
    logging.debug(f"OBJ Path: {obj_path}")
    logging.debug(f"NII Path: {nii_path}")

    obj_dir = os.path.dirname(obj_path)
    if not os.path.exists(obj_dir):
        os.makedirs(obj_dir)

    nii_dir = os.path.dirname(nii_path)
    if not os.path.exists(nii_dir):
        os.makedirs(nii_dir)

    seg_workflow(dcm_path, obj_path, nii_path)
    if os.path.exists(obj_path):
        return jsonify({"msg": "success"})
    else:
        return jsonify({"msg": "failed"})


@app.route('/segVtk', methods=['POST'])
def segVtk():
    dcm_path = request.json['dcm_path']
    obj_path = request.json['obj_path']

    # change path from ubuntu to windows
    # dcm_path = dcm_path.replace("/home/work-temp", "Y:").replace("/", "\\")
    # obj_path = obj_path.replace("/home/work-temp", "Y:").replace("/", "\\")

    logging.debug(f"DCM Path: {dcm_path}")
    logging.debug(f"OBJ Path: {obj_path}")

    obj_dir = os.path.dirname(obj_path)
    if not os.path.exists(obj_dir):
        os.makedirs(obj_dir)

    vtk_workflow(dcm_path, obj_path)
    if os.path.exists(obj_path):
        return jsonify({"msg": "success"})
    else:
        return jsonify({"msg": "failed"})


if __name__ == '__main__':
    port = 4000
    app.run(host='0.0.0.0', port=port, debug=True)
