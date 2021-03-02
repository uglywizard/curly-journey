import base64
import json

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/pubsub/push", methods=["POST"])
def pubsub_push():
    envelope = json.loads(request.data.decode("ascii"))
    payload = base64.b64decode(envelope["message"]["data"])

    # Returning any 2xx status indicates successful receipt of the message.
    return "OK", 200
