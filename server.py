from flask import Flask, jsonify, request
from http import HTTPStatus
from dotenv import load_dotenv
from openai import OpenAI
import os

app = Flask(__name__)

load_dotenv()

key = os.getenv("OPENAI_KEY")
print(key)

client = OpenAI(api_key=key)

assistantId = "asst_9gQjGfbaDczZNzKFSvEwQPAy"

@app.route('/api/stt/threads', methods=['POST'])
def createSttThread():
    print("createSttThread 호출")
    data = request.json
    
    if not data or 'situation' not in data:
        return jsonify({"error": "Invalid request data"}), HTTPStatus.BAD_REQUEST

    try:
        thread = client.beta.threads.create()

        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=f"서비스 : '{data['situation']}'"
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistantId
        )
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        while run.status == 'in_progress':
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            bf = messages.data[0].content[0].text.value
            print(bf)
            return jsonify({"threadId": thread.id, "botFirstMessage": bf}), HTTPStatus.CREATED
        else:
            print(run.status)
            return jsonify({"error": f"Run failed with status: {run.status}"}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/stt/threads/<threadId>', methods=['POST'])
def chatSttThread(threadId):
    data = request.json
    
    if not data or 'userMessage' not in data:
        return jsonify({"error": "Invalid request data"}), HTTPStatus.BAD_REQUEST

    try:
        message = client.beta.threads.messages.create(
            thread_id=threadId,
            role="user",
            content=data['userMessage']
        )
        run = client.beta.threads.runs.create(
            thread_id=threadId,
            assistant_id=assistantId
        )
        run = client.beta.threads.runs.retrieve(thread_id=threadId, run_id=run.id)
        while run.status == 'in_progress':
            run = client.beta.threads.runs.retrieve(thread_id=threadId, run_id=run.id)

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=threadId
            )
            bm = messages.data[0].content[0].text.value
            print(bm)
            return jsonify({"botMessage": bm}), HTTPStatus.OK
        else:
            print(run.status)
            return jsonify({"error": f"Run failed with status: {run.status}"}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/api/stt/threads/<threadId>', methods=['DELETE'])
def finishSttThread(threadId):
    try:
        message = client.beta.threads.messages.create(
            thread_id=threadId,
            role="user",
            content="서비스 : '상황 학습 종료, 피드백 요청'"
        )
        run = client.beta.threads.runs.create(
            thread_id=threadId,
            assistant_id=assistantId
        )
        run = client.beta.threads.runs.retrieve(thread_id=threadId, run_id=run.id)
        while run.status == 'in_progress':
            run = client.beta.threads.runs.retrieve(thread_id=threadId, run_id=run.id)

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=threadId
            )
            fb = messages.data[0].content[0].text.value
            print(fb)
            return jsonify({"feedBack": fb}), HTTPStatus.OK
        else:
            print(run.status)
            return jsonify({"error": f"Run failed with status: {run.status}"}), HTTPStatus.INTERNAL_SERVER_ERROR
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')