import os

import flask
from flask import request, jsonify

from utils.seg import segmentation, seg_workflow
from utils.nii_2_obj import nii_2_obj

app = flask.Flask(__name__)


@app.route('/seg', methods=['POST'])
def seg():
    dcm_path = request.json['dcm_path']
    obj_path = request.json['obj_path']
    nii_path = request.json['nii_path']
    seg_workflow(dcm_path, obj_path, nii_path)
    if os.path.exists(obj_path):
        return jsonify({"msg": "success"})
    else:
        return jsonify({"msg": "failed"})


if __name__ == '__main__':
    port = 5000
    app.run(host='0.0.0.0', port=port)
