import flask
from utils.ar_planner_control import editInputVolumePath, editInputSelector
from utils.igt_control import addConnector, selectIO

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


if __name__ == '__main__':
    app.run()
