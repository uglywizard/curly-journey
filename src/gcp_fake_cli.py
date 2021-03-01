import argparse

from google.cloud import pubsub_v1


def create_subscription(project_id, topic_id, subscription_id):
    """Create a new pull subscription on the given topic."""

    subscriber = pubsub_v1.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic_id)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Wrap the subscriber in a 'with' block to automatically call close() to
    # close the underlying gRPC channel when done.
    with subscriber:
        subscription = subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )

    print(f"Subscription created: {subscription}")


def create_topic(project_id, topic_id):
    """Create a new Pub/Sub topic."""

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    topic = publisher.create_topic(request={"name": topic_path})

    print(f"Created topic: {topic.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("project_id", help="Google Cloud project ID")

    subparsers = parser.add_subparsers(dest="command")

    create_topic_parser = subparsers.add_parser(
        "create-topic", help=create_topic.__doc__
    )
    create_topic_parser.add_argument("topic_id")

    create_subscription_parser = subparsers.add_parser(
        "create-subscription",
        help=create_subscription.__doc__,
    )
    create_subscription_parser.add_argument("topic_id")
    create_subscription_parser.add_argument("subscription_id")

    args = parser.parse_args()

    if args.command == "create-topic":
        create_topic(args.project_id, args.topic_id)
    elif args.command == "create-subscription":
        create_subscription(args.project_id, args.topic_id, args.subscription_id)
