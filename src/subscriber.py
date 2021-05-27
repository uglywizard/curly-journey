import argparse
import time

from base64 import b64decode
from google.cloud import pubsub_v1


def subscription(project_id, subscription_id, sleep=None):
    """Receives messages from a Pub/Sub subscription."""

    def callback(message):
        print(f"Received message: {b64decode(message.data)}")
        if message.attributes:
            print("Message attributes:")
            for attr in message.attributes:
                value = message.attributes.get(attr)
                print(f"{attr}: {value}")
        message.ack()
        print(f"Acknowledged {message.message_id}.")

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    subscriber.subscribe(subscription_path, callback=callback)

    while True:
        time.sleep(sleep)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")
    parser.add_argument("subscription_id", help="Pub/Sub subscription ID")
    parser.add_argument(
        "sleep",
        default=30,
        nargs="?",
        help="Value in seconds to mitigate listening on topic subscription updates. (Default = 30)",
        type=int,
    )

    args = parser.parse_args()

    subscription(args.project_id, args.subscription_id, args.sleep)