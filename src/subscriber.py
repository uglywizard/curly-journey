import argparse
import time

from google.cloud import pubsub_v1


def sub(project_id, subscription_id, sleep=None):
    """Receives messages from a Pub/Sub subscription."""

    def callback(message):
        print(f"Received message: {message.data.decode('ascii')}")
        if message.attributes:
            print("Message attributes:")
            for attr in message.attributes:
                value = message.attributes.get(attr)
                print(f"{attr}: {value}")
        message.ack()
        print(f"Acknowledged {message.message_id}.")

    subscriber_client = pubsub_v1.SubscriberClient()
    subscription_path = subscriber_client.subscription_path(project_id, subscription_id)

    subscriber_client.subscribe(subscription_path, callback=callback)

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
        help="Value in seconds to mitigate listening on topic subscription updates.",
        type=int,
    )

    args = parser.parse_args()

    sub(args.project_id, args.subscription_id, args.sleep)