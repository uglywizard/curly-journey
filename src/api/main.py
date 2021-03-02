import base64
import json

from flask import Flask, request

app = Flask(__name__)

app.debug = True

QUEUE = []


@app.route("/pubsub/push", methods=["POST"])
def pubsub_push():
    envelope = json.loads(request.data.decode("ascii"))
    payload = base64.b64decode(envelope["message"]["data"]).decode("ascii")

    QUEUE.append(payload)

    print(f"Msg: {payload}")

    # Returning any 2xx status indicates successful receipt of the message.
    return "OK", 200
