from flask import Flask, jsonify, request
from http import HTTPStatus
app = Flask(__name__)

@app.route('/api/stt/threads',methods=['POST'])
def mkSttThreads():
    print("X : ")
    return jsonify({"data": "STT", "status" : HTTPStatus.OK})

@app.route('/api/situation/threads', methods=['POST'])
def mkSituationThreads():
    return jsonify({"data": 'SITUATION', "status" : HTTPStatus.OK})

@app.route('/api/advice/threads', methods=['POST'])
def mkAdviceThreads():
    return jsonify({"data": 'ADVICE', "status" : HTTPStatus.OK})


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0')
