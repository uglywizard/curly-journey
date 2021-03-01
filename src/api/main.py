import base64
import json

from flask import Flask
from requests import request

app = Flask(__name__)

MESSAGES = []


@app.route("/pubsub/push", methods=["POST"])
def pubsub_push():
    envelope = json.loads(request.data.decode("utf-8"))
    payload = base64.b64decode(envelope["message"]["data"])

    MESSAGES.append(payload)

    # Returning any 2xx status indicates successful receipt of the message.
    return "OK", 200
